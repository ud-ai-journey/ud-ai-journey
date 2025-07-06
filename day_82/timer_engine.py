import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import json

class TimerType(Enum):
    COUNTDOWN = "countdown"
    COUNTUP = "countup"
    CLOCK = "clock"
    HIDDEN = "hidden"

class TimerState(Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
    FINISHED = "finished"

@dataclass
class TimerConfig:
    id: str
    title: str
    duration: int  # seconds
    timer_type: TimerType
    wrap_up_yellow: int = 60
    wrap_up_red: int = 30
    auto_start: bool = False
    auto_stop: bool = True
    allow_overtime: bool = False
    settings: dict = None

class TimerEngine:
    def __init__(self):
        self.timers: Dict[str, 'Timer'] = {}
        self.callbacks: Dict[str, List[Callable]] = {}
        self._running = False
        self._task = None
    
    def add_timer(self, config: TimerConfig) -> 'Timer':
        """Add a new timer to the engine"""
        timer = Timer(config)
        self.timers[config.id] = timer
        self.callbacks[config.id] = []
        return timer
    
    def remove_timer(self, timer_id: str):
        """Remove a timer from the engine"""
        if timer_id in self.timers:
            timer = self.timers[timer_id]
            timer.stop()
            del self.timers[timer_id]
            if timer_id in self.callbacks:
                del self.callbacks[timer_id]
    
    def get_timer(self, timer_id: str) -> Optional['Timer']:
        """Get a timer by ID"""
        return self.timers.get(timer_id)
    
    def get_all_timers(self) -> List['Timer']:
        """Get all timers"""
        return list(self.timers.values())
    
    def add_callback(self, timer_id: str, callback: Callable):
        """Add a callback for timer updates"""
        if timer_id not in self.callbacks:
            self.callbacks[timer_id] = []
        self.callbacks[timer_id].append(callback)
    
    def remove_callback(self, timer_id: str, callback: Callable):
        """Remove a callback"""
        if timer_id in self.callbacks and callback in self.callbacks[timer_id]:
            self.callbacks[timer_id].remove(callback)
    
    async def start_engine(self):
        """Start the timer engine"""
        if self._running:
            return
        
        self._running = True
        self._task = asyncio.create_task(self._run_engine())
    
    async def stop_engine(self):
        """Stop the timer engine"""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
    
    async def _run_engine(self):
        """Main engine loop"""
        while self._running:
            current_time = time.time()
            
            for timer in self.timers.values():
                if timer.state == TimerState.RUNNING:
                    timer._update(current_time)
                    
                    # Notify callbacks
                    if timer.id in self.callbacks:
                        for callback in self.callbacks[timer.id]:
                            try:
                                await callback(timer)
                            except Exception as e:
                                print(f"Error in timer callback: {e}")
            
            await asyncio.sleep(0.1)  # 10 FPS update rate

class Timer:
    def __init__(self, config: TimerConfig):
        self.id = config.id
        self.title = config.title
        self.duration = config.duration
        self.timer_type = config.timer_type
        self.wrap_up_yellow = config.wrap_up_yellow
        self.wrap_up_red = config.wrap_up_red
        self.auto_start = config.auto_start
        self.auto_stop = config.auto_stop
        self.allow_overtime = config.allow_overtime
        self.settings = config.settings or {}
        
        # State
        self.state = TimerState.STOPPED
        self.current_time = 0
        self.start_time = None
        self.pause_time = None
        self.total_paused_time = 0
        
    def start(self):
        """Start the timer"""
        if self.state == TimerState.RUNNING:
            return
        
        if self.state == TimerState.STOPPED:
            self.current_time = 0 if self.timer_type == TimerType.COUNTDOWN else self.duration
            self.start_time = time.time()
            self.total_paused_time = 0
        elif self.state == TimerState.PAUSED:
            # Resume from pause
            self.total_paused_time += time.time() - self.pause_time
            self.start_time = time.time() - (self.current_time if self.timer_type == TimerType.COUNTDOWN else (self.duration - self.current_time))
        
        self.state = TimerState.RUNNING
        self.pause_time = None
    
    def stop(self):
        """Stop the timer"""
        self.state = TimerState.STOPPED
        self.start_time = None
        self.pause_time = None
        self.total_paused_time = 0
    
    def pause(self):
        """Pause the timer"""
        if self.state == TimerState.RUNNING:
            self.state = TimerState.PAUSED
            self.pause_time = time.time()
    
    def reset(self):
        """Reset the timer to initial state"""
        self.stop()
        if self.timer_type == TimerType.COUNTDOWN:
            self.current_time = 0
        else:
            self.current_time = self.duration
    
    def add_time(self, seconds: int):
        """Add or subtract time from the timer"""
        if self.timer_type == TimerType.COUNTDOWN:
            self.current_time = max(0, self.current_time + seconds)
        else:
            self.current_time = max(0, self.current_time - seconds)
    
    def _update(self, current_time: float):
        """Update timer state (called by engine)"""
        if self.state != TimerState.RUNNING:
            return
        
        elapsed = current_time - self.start_time - self.total_paused_time
        
        if self.timer_type == TimerType.COUNTDOWN:
            self.current_time = max(0, self.duration - elapsed)
            if self.current_time == 0 and self.auto_stop and not self.allow_overtime:
                self.state = TimerState.FINISHED
        elif self.timer_type == TimerType.COUNTUP:
            self.current_time = elapsed
        elif self.timer_type == TimerType.CLOCK:
            # Clock shows current time
            now = datetime.now()
            self.current_time = now.hour * 3600 + now.minute * 60 + now.second
    
    def get_display_time(self) -> str:
        """Get formatted time string for display"""
        if self.timer_type == TimerType.CLOCK:
            now = datetime.now()
            return now.strftime("%H:%M:%S")
        
        total_seconds = int(self.current_time)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def get_warning_level(self) -> str:
        """Get warning level for display (normal, yellow, red)"""
        if self.timer_type != TimerType.COUNTDOWN:
            return "normal"
        
        if self.current_time <= self.wrap_up_red:
            return "red"
        elif self.current_time <= self.wrap_up_yellow:
            return "yellow"
        else:
            return "normal"
    
    def to_dict(self) -> dict:
        """Convert timer to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "duration": self.duration,
            "timer_type": self.timer_type.value,
            "current_time": self.current_time,
            "display_time": self.get_display_time(),
            "warning_level": self.get_warning_level(),
            "state": self.state.value,
            "wrap_up_yellow": self.wrap_up_yellow,
            "wrap_up_red": self.wrap_up_red,
            "settings": self.settings
        } 