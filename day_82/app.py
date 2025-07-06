from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import uuid
import json
from typing import Optional
from datetime import datetime
import os

from models import Base, Room, Timer, Message, ConnectedDevice
from timer_engine import TimerEngine, TimerConfig, TimerType
from websocket_manager import ConnectionManager, WebSocketHandler

# Pydantic models for request/response
class TimerCreate(BaseModel):
    title: str
    duration: int
    timer_type: str = "countdown"
    wrap_up_yellow: int = 60
    wrap_up_red: int = 30

class MessageCreate(BaseModel):
    content: str
    color: str = "#ffffff"
    is_bold: bool = False
    is_uppercase: bool = False
    is_flashing: bool = False

class TimerControl(BaseModel):
    action: str
    data: Optional[dict] = None

# Create FastAPI app
app = FastAPI(title="SyncStage", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
timer_engine = TimerEngine()
connection_manager = ConnectionManager()
websocket_handler = WebSocketHandler(connection_manager, timer_engine)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# In-memory storage for rooms (in production, use database)
rooms = {}

@app.on_event("startup")
async def startup_event():
    """Start the timer engine on startup"""
    await timer_engine.start_engine()

@app.on_event("shutdown")
async def shutdown_event():
    """Stop the timer engine on shutdown"""
    await timer_engine.stop_engine()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with room creation"""
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/api/rooms")
async def create_room(title: str = Form(...), password: Optional[str] = Form(None)):
    """Create a new room"""
    room_id = str(uuid.uuid4())
    
    room = {
        "id": room_id,
        "title": title,
        "password": password,
        "created_at": datetime.now().isoformat(),
        "timers": []
    }
    
    rooms[room_id] = room
    
    return {
        "room_id": room_id,
        "title": title,
        "controller_url": f"/controller/{room_id}",
        "viewer_url": f"/viewer/{room_id}",
        "agenda_url": f"/agenda/{room_id}"
    }

@app.get("/controller/{room_id}", response_class=HTMLResponse)
async def controller_page(request: Request, room_id: str):
    """Controller interface for managing timers"""
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    
    room = rooms[room_id]
    return templates.TemplateResponse("controller.html", {
        "request": request,
        "room": room
    })

@app.get("/viewer/{room_id}", response_class=HTMLResponse)
async def viewer_page(request: Request, room_id: str):
    """Viewer interface for displaying timers"""
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    
    room = rooms[room_id]
    return templates.TemplateResponse("viewer.html", {
        "request": request,
        "room": room
    })

@app.get("/agenda/{room_id}", response_class=HTMLResponse)
async def agenda_page(request: Request, room_id: str):
    """Agenda page for event participants"""
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    
    room = rooms[room_id]
    return templates.TemplateResponse("agenda.html", {
        "request": request,
        "room": room
    })

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    room_id: str, 
    device_type: str = "viewer",
    device_name: Optional[str] = None
):
    """WebSocket endpoint for real-time communication"""
    if room_id not in rooms:
        await websocket.close(code=4004, reason="Room not found")
        return
    
    await websocket_handler.handle_websocket(websocket, room_id, device_type, device_name or "Unknown Device")

@app.post("/api/rooms/{room_id}/timers")
async def create_timer(room_id: str, timer_data: TimerCreate):
    """Create a new timer in a room"""
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    
    timer_id = str(uuid.uuid4())
    
    # Create timer config
    config = TimerConfig(
        id=timer_id,
        title=timer_data.title,
        duration=timer_data.duration,
        timer_type=TimerType(timer_data.timer_type),
        wrap_up_yellow=timer_data.wrap_up_yellow,
        wrap_up_red=timer_data.wrap_up_red
    )
    
    # Add timer to engine
    timer = timer_engine.add_timer(config)
    
    # Add to room
    timer_info = {
        "id": timer_id,
        "title": timer_data.title,
        "duration": timer_data.duration,
        "timer_type": timer_data.timer_type,
        "wrap_up_yellow": timer_data.wrap_up_yellow,
        "wrap_up_red": timer_data.wrap_up_red,
        "position": len(rooms[room_id]["timers"])
    }
    
    rooms[room_id]["timers"].append(timer_info)
    
    return {"timer_id": timer_id, "timer": timer_info}

@app.get("/api/rooms/{room_id}/timers")
async def get_timers(room_id: str):
    """Get all timers in a room"""
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return {"timers": rooms[room_id]["timers"]}

@app.post("/api/rooms/{room_id}/timers/{timer_id}/control")
async def control_timer(room_id: str, timer_id: str, control_data: TimerControl):
    """Control a timer (start, stop, pause, reset, add_time)"""
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    
    timer = timer_engine.get_timer(timer_id)
    if not timer:
        raise HTTPException(status_code=404, detail="Timer not found")
    
    # Execute action
    if control_data.action == "start":
        timer.start()
    elif control_data.action == "stop":
        timer.stop()
    elif control_data.action == "pause":
        timer.pause()
    elif control_data.action == "reset":
        timer.reset()
    elif control_data.action == "add_time":
        seconds = control_data.data.get("seconds", 0) if control_data.data else 0
        timer.add_time(seconds)
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    # Broadcast to all devices in room
    await connection_manager.broadcast_timer_control(room_id, control_data.action, timer_id, control_data.data or {})
    await connection_manager.broadcast_timer_update(room_id, timer.to_dict())
    
    return {"success": True, "timer": timer.to_dict()}

@app.post("/api/rooms/{room_id}/messages")
async def create_message(room_id: str, message_data: MessageCreate):
    """Create a display message"""
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    
    message_info = {
        "id": str(uuid.uuid4()),
        "content": message_data.content,
        "color": message_data.color,
        "is_bold": message_data.is_bold,
        "is_uppercase": message_data.is_uppercase,
        "is_flashing": message_data.is_flashing,
        "created_at": datetime.now().isoformat()
    }
    
    # Broadcast message to all viewers
    await connection_manager.broadcast_message(room_id, message_info)
    
    return {"message": message_info}

@app.get("/api/rooms/{room_id}/devices")
async def get_devices(room_id: str):
    """Get all connected devices in a room"""
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    
    devices = connection_manager.get_room_devices(room_id)
    return {"devices": devices}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 