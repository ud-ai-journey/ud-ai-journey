from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()

class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    password_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    settings = Column(JSON, default=dict)

class Timer(Base):
    __tablename__ = "timers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    room_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  # Duration in seconds
    start_time = Column(DateTime, nullable=True)
    timer_type = Column(String, default="countdown")  # countdown, countup, clock, hidden
    wrap_up_yellow = Column(Integer, default=60)  # Seconds before zero to show yellow
    wrap_up_red = Column(Integer, default=30)  # Seconds before zero to show red
    position = Column(Integer, default=0)  # Order in sequence
    settings = Column(JSON, default=dict)
    is_active = Column(Boolean, default=False)
    current_time = Column(Integer, default=0)  # Current time in seconds
    is_running = Column(Boolean, default=False)
    started_at = Column(DateTime, nullable=True)

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    room_id = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    color = Column(String, default="#ffffff")
    is_bold = Column(Boolean, default=False)
    is_uppercase = Column(Boolean, default=False)
    is_flashing = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=True)

class ConnectedDevice(Base):
    __tablename__ = "connected_devices"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    room_id = Column(String, nullable=False)
    device_name = Column(String, nullable=False)
    device_type = Column(String, default="viewer")  # controller, viewer, moderator
    last_seen = Column(DateTime, default=func.now())
    session_id = Column(String, nullable=False)
    ip_address = Column(String, nullable=True) 