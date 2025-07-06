import asyncio
import json
import uuid
from typing import Dict, Set, Optional, Any
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.room_devices: Dict[str, Dict[str, dict]] = {}
        self.connection_info: Dict[WebSocket, dict] = {}
    
    async def connect(self, websocket: WebSocket, room_id: str, device_type: str = "viewer", device_name: str = None):
        """Connect a new WebSocket to a room"""
        await websocket.accept()
        
        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()
            self.room_devices[room_id] = {}
        
        self.active_connections[room_id].add(websocket)
        
        # Generate device info
        device_id = str(uuid.uuid4())
        device_info = {
            "id": device_id,
            "name": device_name or f"{device_type.title()} {len(self.room_devices[room_id]) + 1}",
            "type": device_type,
            "connected_at": datetime.now().isoformat(),
            "last_seen": datetime.now().isoformat()
        }
        
        self.room_devices[room_id][device_id] = device_info
        self.connection_info[websocket] = {
            "room_id": room_id,
            "device_id": device_id,
            "device_type": device_type
        }
        
        # Send welcome message
        await websocket.send_text(json.dumps({
            "type": "welcome",
            "device_id": device_id,
            "room_id": room_id,
            "devices": list(self.room_devices[room_id].values())
        }))
        
        # Notify other devices
        await self.broadcast_to_room(room_id, {
            "type": "device_connected",
            "device": device_info
        }, exclude_websocket=websocket)
        
        logger.info(f"Device {device_id} connected to room {room_id}")
        return device_id
    
    async def disconnect(self, websocket: WebSocket):
        """Disconnect a WebSocket"""
        if websocket not in self.connection_info:
            return
        
        info = self.connection_info[websocket]
        room_id = info["room_id"]
        device_id = info["device_id"]
        
        # Remove from active connections
        if room_id in self.active_connections:
            self.active_connections[room_id].discard(websocket)
            
            # Remove device info
            if room_id in self.room_devices and device_id in self.room_devices[room_id]:
                device_info = self.room_devices[room_id][device_id]
                del self.room_devices[room_id][device_id]
                
                # Notify other devices
                await self.broadcast_to_room(room_id, {
                    "type": "device_disconnected",
                    "device_id": device_id,
                    "device_name": device_info["name"]
                })
        
        # Clean up connection info
        del self.connection_info[websocket]
        
        # Clean up empty rooms
        if room_id in self.active_connections and not self.active_connections[room_id]:
            del self.active_connections[room_id]
            if room_id in self.room_devices:
                del self.room_devices[room_id]
        
        logger.info(f"Device {device_id} disconnected from room {room_id}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific WebSocket"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            await self.disconnect(websocket)
    
    async def broadcast_to_room(self, room_id: str, message: dict, exclude_websocket: WebSocket = None):
        """Broadcast a message to all connections in a room"""
        if room_id not in self.active_connections:
            return
        
        disconnected = set()
        for websocket in self.active_connections[room_id]:
            if websocket == exclude_websocket:
                continue
            
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting to room {room_id}: {e}")
                disconnected.add(websocket)
        
        # Clean up disconnected websockets
        for websocket in disconnected:
            await self.disconnect(websocket)
    
    async def broadcast_timer_update(self, room_id: str, timer_data: dict):
        """Broadcast timer updates to all viewers in a room"""
        message = {
            "type": "timer_update",
            "timer": timer_data
        }
        await self.broadcast_to_room(room_id, message)
    
    async def broadcast_timer_control(self, room_id: str, action: str, timer_id: str, data: dict = None):
        """Broadcast timer control actions to all devices in a room"""
        message = {
            "type": "timer_control",
            "action": action,
            "timer_id": timer_id,
            "data": data or {}
        }
        await self.broadcast_to_room(room_id, message)
    
    async def broadcast_message(self, room_id: str, message_data: dict):
        """Broadcast a display message to all viewers in a room"""
        message = {
            "type": "display_message",
            "message": message_data
        }
        await self.broadcast_to_room(room_id, message)
    
    def get_room_devices(self, room_id: str) -> list:
        """Get all devices connected to a room"""
        if room_id not in self.room_devices:
            return []
        return list(self.room_devices[room_id].values())
    
    def get_room_connection_count(self, room_id: str) -> int:
        """Get the number of connections in a room"""
        if room_id not in self.active_connections:
            return 0
        return len(self.active_connections[room_id])
    
    def update_device_seen(self, websocket: WebSocket):
        """Update the last seen time for a device"""
        if websocket in self.connection_info:
            info = self.connection_info[websocket]
            room_id = info["room_id"]
            device_id = info["device_id"]
            
            if room_id in self.room_devices and device_id in self.room_devices[room_id]:
                self.room_devices[room_id][device_id]["last_seen"] = datetime.now().isoformat()

class WebSocketHandler:
    def __init__(self, connection_manager: ConnectionManager, timer_engine):
        self.connection_manager = connection_manager
        self.timer_engine = timer_engine
    
    async def handle_websocket(self, websocket: WebSocket, room_id: str, device_type: str = "viewer", device_name: str = None):
        """Handle a WebSocket connection"""
        device_id = await self.connection_manager.connect(websocket, room_id, device_type, device_name)
        
        try:
            while True:
                # Update last seen
                self.connection_manager.update_device_seen(websocket)
                
                # Receive message
                data = await websocket.receive_text()
                message = json.loads(data)
                
                await self.handle_message(websocket, message)
                
        except WebSocketDisconnect:
            await self.connection_manager.disconnect(websocket)
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            await self.connection_manager.disconnect(websocket)
    
    async def handle_message(self, websocket: WebSocket, message: dict):
        """Handle incoming WebSocket messages"""
        message_type = message.get("type")
        
        if message_type == "timer_control":
            await self.handle_timer_control(websocket, message)
        elif message_type == "display_message":
            await self.handle_display_message(websocket, message)
        elif message_type == "device_update":
            await self.handle_device_update(websocket, message)
        elif message_type == "ping":
            await self.connection_manager.send_personal_message({"type": "pong"}, websocket)
        else:
            logger.warning(f"Unknown message type: {message_type}")
    
    async def handle_timer_control(self, websocket: WebSocket, message: dict):
        """Handle timer control messages"""
        action = message.get("action")
        timer_id = message.get("timer_id")
        data = message.get("data", {})
        
        if not timer_id:
            return
        
        timer = self.timer_engine.get_timer(timer_id)
        if not timer:
            return
        
        # Get room info
        if websocket not in self.connection_manager.connection_info:
            return
        
        room_id = self.connection_manager.connection_info[websocket]["room_id"]
        
        # Execute timer action
        if action == "start":
            timer.start()
        elif action == "stop":
            timer.stop()
        elif action == "pause":
            timer.pause()
        elif action == "reset":
            timer.reset()
        elif action == "add_time":
            seconds = data.get("seconds", 0)
            timer.add_time(seconds)
        
        # Broadcast the control action to all devices
        await self.connection_manager.broadcast_timer_control(room_id, action, timer_id, data)
        
        # Broadcast updated timer state
        await self.connection_manager.broadcast_timer_update(room_id, timer.to_dict())
    
    async def handle_display_message(self, websocket: WebSocket, message: dict):
        """Handle display message requests"""
        message_data = message.get("message", {})
        
        if websocket not in self.connection_manager.connection_info:
            return
        
        room_id = self.connection_manager.connection_info[websocket]["room_id"]
        
        # Broadcast message to all viewers
        await self.connection_manager.broadcast_message(room_id, message_data)
    
    async def handle_device_update(self, websocket: WebSocket, message: dict):
        """Handle device information updates"""
        if websocket not in self.connection_manager.connection_info:
            return
        
        info = self.connection_manager.connection_info[websocket]
        room_id = info["room_id"]
        device_id = info["device_id"]
        
        # Update device info
        if room_id in self.connection_manager.room_devices and device_id in self.connection_manager.room_devices[room_id]:
            device_info = self.connection_manager.room_devices[room_id][device_id]
            device_info.update(message.get("device", {}))
            device_info["last_seen"] = datetime.now().isoformat()
            
            # Broadcast device update
            await self.connection_manager.broadcast_to_room(room_id, {
                "type": "device_updated",
                "device": device_info
            }, exclude_websocket=websocket) 