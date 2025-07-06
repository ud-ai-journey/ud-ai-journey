// Viewer JavaScript
class Viewer {
    constructor() {
        this.roomId = window.location.pathname.split('/')[2];
        this.websocket = null;
        this.currentTimer = null;
        this.currentMessage = null;
        this.isConnected = false;
        this.isFullscreen = false;
        this.isBlackout = false;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.connectWebSocket();
        this.setupFullscreenHandlers();
    }
    
    setupEventListeners() {
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case 'F11':
                    e.preventDefault();
                    this.toggleFullscreen();
                    break;
                case 'b':
                case 'B':
                    e.preventDefault();
                    this.toggleBlackout();
                    break;
                case 'Escape':
                    if (this.isFullscreen) {
                        this.exitFullscreen();
                    }
                    break;
            }
        });
        
        // Prevent context menu
        document.addEventListener('contextmenu', (e) => {
            e.preventDefault();
        });
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
            case 'timer_control':
                this.handleTimerControl(message);
                break;
            case 'display_message':
                this.handleDisplayMessage(message.message);
                break;
        }
    }
    
    handleWelcome(message) {
        console.log('Connected to room:', message.room_id);
    }
    
    handleTimerUpdate(timerData) {
        this.currentTimer = timerData;
        this.updateTimerDisplay();
    }
    
    handleTimerControl(message) {
        // Update timer based on control action
        if (this.currentTimer && this.currentTimer.id === message.timer_id) {
            this.updateTimerDisplay();
        }
    }
    
    handleDisplayMessage(messageData) {
        this.currentMessage = messageData;
        this.updateMessageDisplay();
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
    
    updateTimerDisplay() {
        const titleElement = document.getElementById('timerTitle');
        const timeElement = document.getElementById('timerTime');
        const progressElement = document.getElementById('progressBar');
        const fullscreenTitle = document.getElementById('fullscreenTitle');
        const fullscreenTime = document.getElementById('fullscreenTime');
        
        if (!this.currentTimer) {
            titleElement.textContent = 'No Active Timer';
            timeElement.textContent = '--:--';
            progressElement.style.width = '0%';
            fullscreenTitle.textContent = 'No Active Timer';
            fullscreenTime.textContent = '--:--';
            return;
        }
        
        const timer = this.currentTimer;
        
        // Update title
        titleElement.textContent = timer.title;
        fullscreenTitle.textContent = timer.title;
        
        // Update time
        timeElement.textContent = timer.display_time;
        fullscreenTime.textContent = timer.display_time;
        
        // Update warning colors
        timeElement.className = `timer-time ${this.getWarningClass(timer)}`;
        fullscreenTime.className = `fullscreen-time ${this.getWarningClass(timer)}`;
        
        // Update progress bar
        const progressWidth = this.getProgressWidth(timer);
        progressElement.style.width = `${progressWidth}%`;
        progressElement.className = `progress-bar ${this.getWarningClass(timer)}`;
    }
    
    updateMessageDisplay() {
        const messageDisplay = document.getElementById('messageDisplay');
        const messageContent = document.getElementById('messageContent');
        const fullscreenMessage = document.getElementById('fullscreenMessage');
        
        if (!this.currentMessage || !this.currentMessage.content) {
            messageDisplay.classList.remove('show');
            fullscreenMessage.textContent = '';
            return;
        }
        
        const message = this.currentMessage;
        
        // Set message content
        messageContent.textContent = message.content;
        fullscreenMessage.textContent = message.content;
        
        // Apply styling
        messageContent.style.color = message.color;
        fullscreenMessage.style.color = message.color;
        
        if (message.is_bold) {
            messageContent.style.fontWeight = 'bold';
            fullscreenMessage.style.fontWeight = 'bold';
        } else {
            messageContent.style.fontWeight = 'normal';
            fullscreenMessage.style.fontWeight = 'normal';
        }
        
        if (message.is_uppercase) {
            messageContent.style.textTransform = 'uppercase';
            fullscreenMessage.style.textTransform = 'uppercase';
        } else {
            messageContent.style.textTransform = 'none';
            fullscreenMessage.style.textTransform = 'none';
        }
        
        if (message.is_flashing) {
            messageContent.classList.add('flashing');
            fullscreenMessage.classList.add('flashing');
        } else {
            messageContent.classList.remove('flashing');
            fullscreenMessage.classList.remove('flashing');
        }
        
        // Show message
        messageDisplay.classList.add('show');
        
        // Auto-hide message after 10 seconds (unless it's flashing)
        if (!message.is_flashing) {
            setTimeout(() => {
                messageDisplay.classList.remove('show');
            }, 10000);
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
    
    setupFullscreenHandlers() {
        // Listen for fullscreen changes
        document.addEventListener('fullscreenchange', () => {
            this.isFullscreen = !!document.fullscreenElement;
            this.updateFullscreenDisplay();
        });
        
        // Listen for webkit fullscreen changes (Safari)
        document.addEventListener('webkitfullscreenchange', () => {
            this.isFullscreen = !!document.webkitFullscreenElement;
            this.updateFullscreenDisplay();
        });
    }
    
    updateFullscreenDisplay() {
        const overlay = document.getElementById('fullscreenOverlay');
        if (this.isFullscreen) {
            overlay.classList.add('show');
        } else {
            overlay.classList.remove('show');
        }
    }
    
    requestFullscreen() {
        const element = document.documentElement;
        
        if (element.requestFullscreen) {
            element.requestFullscreen();
        } else if (element.webkitRequestFullscreen) {
            element.webkitRequestFullscreen();
        } else if (element.msRequestFullscreen) {
            element.msRequestFullscreen();
        }
    }
    
    exitFullscreen() {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
    }
    
    toggleFullscreen() {
        if (this.isFullscreen) {
            this.exitFullscreen();
        } else {
            this.requestFullscreen();
        }
    }
    
    toggleBlackout() {
        const overlay = document.getElementById('blackoutOverlay');
        this.isBlackout = !this.isBlackout;
        
        if (this.isBlackout) {
            overlay.classList.add('show');
        } else {
            overlay.classList.remove('show');
        }
    }
    
    toggleControlPanel() {
        const panel = document.getElementById('controlPanel');
        panel.classList.toggle('show');
    }
}

// Global functions for HTML onclick handlers
function requestFullscreen() {
    viewer.requestFullscreen();
}

function toggleBlackout() {
    viewer.toggleBlackout();
}

function toggleControlPanel() {
    viewer.toggleControlPanel();
}

// Initialize viewer when page loads
let viewer;
document.addEventListener('DOMContentLoaded', () => {
    viewer = new Viewer();
}); 