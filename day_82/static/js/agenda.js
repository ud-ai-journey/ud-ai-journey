// Agenda JavaScript
class Agenda {
    constructor() {
        this.roomId = window.location.pathname.split('/')[2];
        this.websocket = null;
        this.timers = new Map();
        this.devices = new Map();
        this.isConnected = false;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.connectWebSocket();
        this.loadTimers();
        this.loadDevices();
    }
    
    setupEventListeners() {
        // Auto-refresh every 30 seconds
        setInterval(() => {
            this.loadTimers();
            this.loadDevices();
        }, 30000);
    }
    
    connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/${this.roomId}?device_type=viewer`;
        
        this.websocket = new WebSocket(wsUrl);
        
        this.websocket.onopen = () => {
            this.isConnected = true;
            this.updateConnectionStatus('connected');
        };
        
        this.websocket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            this.handleWebSocketMessage(message);
        };
        
        this.websocket.onclose = () => {
            this.isConnected = false;
            this.updateConnectionStatus('disconnected');
            // Reconnect after 5 seconds
            setTimeout(() => this.connectWebSocket(), 5000);
        };
        
        this.websocket.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateConnectionStatus('error');
        };
    }
    
    handleWebSocketMessage(message) {
        switch (message.type) {
            case 'welcome':
                this.handleWelcome(message);
                break;
            case 'timer_update':
                this.handleTimerUpdate(message.timer);
                break;
            case 'device_connected':
                this.handleDeviceConnected(message.device);
                break;
            case 'device_disconnected':
                this.handleDeviceDisconnected(message.device_id);
                break;
        }
    }
    
    handleWelcome(message) {
        console.log('Connected to room:', message.room_id);
    }
    
    handleTimerUpdate(timerData) {
        this.timers.set(timerData.id, timerData);
        this.updateAgendaDisplay();
        this.updateCurrentTimer();
        this.updateProgress();
    }
    
    handleDeviceConnected(device) {
        this.devices.set(device.id, device);
        this.updateDevicesList();
    }
    
    handleDeviceDisconnected(deviceId) {
        this.devices.delete(deviceId);
        this.updateDevicesList();
    }
    
    updateConnectionStatus(status) {
        const statusElement = document.getElementById('connectionStatus');
        const dot = statusElement.querySelector('.status-dot');
        const text = statusElement.querySelector('.status-text');
        
        dot.className = 'status-dot ' + status;
        
        switch (status) {
            case 'connected':
                text.textContent = 'Live';
                break;
            case 'disconnected':
                text.textContent = 'Disconnected';
                break;
            case 'error':
                text.textContent = 'Error';
                break;
            default:
                text.textContent = 'Connecting...';
        }
    }
    
    async loadTimers() {
        try {
            const response = await fetch(`/api/rooms/${this.roomId}/timers`);
            if (response.ok) {
                const data = await response.json();
                this.timers.clear();
                data.timers.forEach(timer => {
                    this.timers.set(timer.id, timer);
                });
                this.updateAgendaDisplay();
                this.updateCurrentTimer();
                this.updateProgress();
            }
        } catch (error) {
            console.error('Error loading timers:', error);
        }
    }
    
    async loadDevices() {
        try {
            const response = await fetch(`/api/rooms/${this.roomId}/devices`);
            if (response.ok) {
                const data = await response.json();
                this.devices.clear();
                data.devices.forEach(device => {
                    this.devices.set(device.id, device);
                });
                this.updateDevicesList();
            }
        } catch (error) {
            console.error('Error loading devices:', error);
        }
    }
    
    updateAgendaDisplay() {
        const timeline = document.getElementById('agendaTimeline');
        const upcomingTimers = document.getElementById('upcomingTimers');
        
        if (this.timers.size === 0) {
            timeline.innerHTML = `
                <div class="no-agenda">
                    <p>No agenda items have been created yet.</p>
                    <p>Check back later for the event schedule.</p>
                </div>
            `;
            upcomingTimers.innerHTML = '<p>No upcoming timers</p>';
            return;
        }
        
        // Sort timers by position
        const sortedTimers = Array.from(this.timers.values()).sort((a, b) => a.position - b.position);
        
        // Update timeline
        timeline.innerHTML = '';
        sortedTimers.forEach((timer, index) => {
            const timelineItem = this.createTimelineItem(timer, index);
            timeline.appendChild(timelineItem);
        });
        
        // Update upcoming timers
        const activeTimer = sortedTimers.find(timer => timer.state === 'running');
        const upcoming = sortedTimers.filter(timer => 
            timer.state === 'stopped' && 
            (!activeTimer || timer.position > activeTimer.position)
        );
        
        upcomingTimers.innerHTML = '';
        if (upcoming.length === 0) {
            upcomingTimers.innerHTML = '<p>No upcoming timers</p>';
        } else {
            upcoming.slice(0, 3).forEach(timer => {
                const upcomingItem = this.createUpcomingItem(timer);
                upcomingTimers.appendChild(upcomingItem);
            });
        }
    }
    
    createTimelineItem(timer, index) {
        const item = document.createElement('div');
        item.className = 'timeline-item';
        
        const status = this.getTimerStatus(timer);
        const duration = this.formatDuration(timer.duration);
        
        item.innerHTML = `
            <div class="timeline-marker ${status}">
                <span class="marker-number">${index + 1}</span>
            </div>
            <div class="timeline-content">
                <div class="timeline-header">
                    <h4 class="timeline-title">${timer.title}</h4>
                    <span class="timeline-duration">${duration}</span>
                </div>
                <div class="timeline-status">
                    <span class="status-badge ${status}">${this.getStatusText(timer)}</span>
                    ${timer.state === 'running' ? `<span class="current-time">${timer.display_time}</span>` : ''}
                </div>
            </div>
        `;
        
        return item;
    }
    
    createUpcomingItem(timer) {
        const item = document.createElement('div');
        item.className = 'upcoming-item';
        
        const duration = this.formatDuration(timer.duration);
        
        item.innerHTML = `
            <div class="upcoming-title">${timer.title}</div>
            <div class="upcoming-duration">${duration}</div>
        `;
        
        return item;
    }
    
    updateCurrentTimer() {
        const currentTimer = Array.from(this.timers.values()).find(timer => timer.state === 'running');
        const titleElement = document.getElementById('currentTimerTitle');
        const timeElement = document.getElementById('currentTimerTime');
        const progressElement = document.getElementById('currentProgressBar');
        
        if (!currentTimer) {
            titleElement.textContent = 'No active timer';
            timeElement.textContent = '--:--';
            progressElement.style.width = '0%';
            return;
        }
        
        titleElement.textContent = currentTimer.title;
        timeElement.textContent = currentTimer.display_time;
        
        // Update progress
        const progressWidth = this.getProgressWidth(currentTimer);
        progressElement.style.width = `${progressWidth}%`;
        progressElement.className = `progress-bar ${this.getWarningClass(currentTimer)}`;
    }
    
    updateProgress() {
        const completedCount = document.getElementById('completedCount');
        const remainingCount = document.getElementById('remainingCount');
        const totalTime = document.getElementById('totalTime');
        
        const timers = Array.from(this.timers.values());
        const completed = timers.filter(timer => timer.state === 'finished').length;
        const remaining = timers.filter(timer => timer.state !== 'finished').length;
        const totalDuration = timers.reduce((sum, timer) => sum + timer.duration, 0);
        
        completedCount.textContent = completed;
        remainingCount.textContent = remaining;
        totalTime.textContent = this.formatDuration(totalDuration);
    }
    
    updateDevicesList() {
        const list = document.getElementById('deviceList');
        
        if (list) {
            list.innerHTML = '';
            this.devices.forEach(device => {
                const deviceItem = document.createElement('div');
                deviceItem.className = 'device-item';
                deviceItem.innerHTML = `
                    <div class="device-info">
                        <span class="device-name">${device.name}</span>
                        <span class="device-type">${device.type}</span>
                    </div>
                    <span class="device-status">Connected</span>
                `;
                list.appendChild(deviceItem);
            });
        }
    }
    
    getTimerStatus(timer) {
        switch (timer.state) {
            case 'running': return 'active';
            case 'finished': return 'completed';
            case 'paused': return 'paused';
            default: return 'pending';
        }
    }
    
    getStatusText(timer) {
        switch (timer.state) {
            case 'running': return 'In Progress';
            case 'finished': return 'Completed';
            case 'paused': return 'Paused';
            default: return 'Pending';
        }
    }
    
    getWarningClass(timer) {
        if (timer.warning_level === 'yellow') return 'warning-yellow';
        if (timer.warning_level === 'red') return 'warning-red';
        return '';
    }
    
    getProgressWidth(timer) {
        if (timer.timer_type === 'countdown') {
            const remaining = timer.current_time;
            const total = timer.duration;
            return Math.max(0, Math.min(100, (remaining / total) * 100));
        }
        return 0;
    }
    
    formatDuration(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        
        if (hours > 0) {
            return `${hours}h ${minutes}m`;
        } else {
            return `${minutes}m`;
        }
    }
}

// Initialize agenda when page loads
let agenda;
document.addEventListener('DOMContentLoaded', () => {
    agenda = new Agenda();
}); 