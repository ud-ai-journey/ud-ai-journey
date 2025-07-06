// Controller JavaScript
class Controller {
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
        // Tab navigation
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });
        
        // Create timer button
        document.getElementById('createTimerBtn').addEventListener('click', () => {
            this.showModal('createTimerModal');
        });
        
        // Modal close buttons
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.closeModal(e.target.closest('.modal').id);
            });
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case '1':
                        e.preventDefault();
                        this.switchTab('timers');
                        break;
                    case '2':
                        e.preventDefault();
                        this.switchTab('messages');
                        break;
                    case '3':
                        e.preventDefault();
                        this.switchTab('devices');
                        break;
                    case '4':
                        e.preventDefault();
                        this.switchTab('settings');
                        break;
                }
            }
        });
    }
    
    connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/${this.roomId}?device_type=controller`;
        
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
            case 'device_updated':
                this.handleDeviceUpdated(message.device);
                break;
        }
    }
    
    handleWelcome(message) {
        this.deviceId = message.device_id;
        this.devices.clear();
        message.devices.forEach(device => {
            this.devices.set(device.id, device);
        });
        this.updateDevicesList();
    }
    
    handleTimerUpdate(timerData) {
        this.timers.set(timerData.id, timerData);
        this.updateTimerDisplay(timerData);
    }
    
    handleDeviceConnected(device) {
        this.devices.set(device.id, device);
        this.updateDevicesList();
    }
    
    handleDeviceDisconnected(deviceId) {
        this.devices.delete(deviceId);
        this.updateDevicesList();
    }
    
    handleDeviceUpdated(device) {
        this.devices.set(device.id, device);
        this.updateDevicesList();
    }
    
    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');
    }
    
    showModal(modalId) {
        document.getElementById(modalId).classList.add('show');
    }
    
    closeModal(modalId) {
        document.getElementById(modalId).classList.remove('show');
    }
    
    updateConnectionStatus(status) {
        const statusElement = document.getElementById('connectionStatus');
        const dot = statusElement.querySelector('.status-dot');
        const text = statusElement.querySelector('.status-text');
        
        dot.className = 'status-dot ' + status;
        
        switch (status) {
            case 'connected':
                text.textContent = 'Connected';
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
                data.timers.forEach(timer => {
                    this.timers.set(timer.id, timer);
                });
                this.updateTimersGrid();
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
    
    updateTimersGrid() {
        const grid = document.getElementById('timersGrid');
        grid.innerHTML = '';
        
        this.timers.forEach(timer => {
            const timerCard = this.createTimerCard(timer);
            grid.appendChild(timerCard);
        });
        
        if (this.timers.size === 0) {
            grid.innerHTML = '<div class="no-timers"><p>No timers created yet. Create your first timer to get started.</p></div>';
        }
    }
    
    createTimerCard(timer) {
        const card = document.createElement('div');
        card.className = 'timer-card';
        if (timer.state === 'running') card.classList.add('active');
        
        card.innerHTML = `
            <div class="timer-header">
                <div class="timer-title">${timer.title}</div>
                <div class="timer-type">${timer.timer_type}</div>
            </div>
            <div class="timer-display">
                <div class="timer-time ${this.getWarningClass(timer)}">${timer.display_time}</div>
                <div class="timer-progress">
                    <div class="progress-bar ${this.getWarningClass(timer)}" style="width: ${this.getProgressWidth(timer)}%"></div>
                </div>
            </div>
            <div class="timer-controls">
                <button class="btn-primary" onclick="controller.controlTimer('${timer.id}', 'start')" ${timer.state === 'running' ? 'disabled' : ''}>Start</button>
                <button class="btn-secondary" onclick="controller.controlTimer('${timer.id}', 'stop')" ${timer.state === 'stopped' ? 'disabled' : ''}>Stop</button>
                <button class="btn-secondary" onclick="controller.controlTimer('${timer.id}', 'pause')" ${timer.state !== 'running' ? 'disabled' : ''}>Pause</button>
                <button class="btn-secondary" onclick="controller.controlTimer('${timer.id}', 'reset')">Reset</button>
            </div>
            <div class="timer-actions">
                <button class="btn-secondary" onclick="controller.addTime('${timer.id}', 60)">+1 Min</button>
                <button class="btn-secondary" onclick="controller.addTime('${timer.id}', -60)">-1 Min</button>
                <button class="btn-secondary" onclick="controller.addTime('${timer.id}', 300)">+5 Min</button>
                <button class="btn-secondary" onclick="controller.addTime('${timer.id}', -300)">-5 Min</button>
            </div>
        `;
        
        return card;
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
    
    updateTimerDisplay(timer) {
        const existingCard = document.querySelector(`[data-timer-id="${timer.id}"]`);
        if (existingCard) {
            const newCard = this.createTimerCard(timer);
            existingCard.replaceWith(newCard);
        } else {
            this.updateTimersGrid();
        }
    }
    
    updateDevicesList() {
        const list = document.getElementById('devicesList');
        const count = document.getElementById('deviceCount');
        
        if (list) {
            list.innerHTML = '';
            this.devices.forEach(device => {
                const deviceItem = document.createElement('div');
                deviceItem.className = 'device-item';
                deviceItem.innerHTML = `
                    <div class="device-info">
                        <div class="device-name">${device.name}</div>
                        <div class="device-type">${device.type}</div>
                    </div>
                    <div class="device-status">Connected</div>
                `;
                list.appendChild(deviceItem);
            });
        }
        
        if (count) {
            count.textContent = this.devices.size;
        }
    }
    
    async controlTimer(timerId, action, data = {}) {
        try {
            const response = await fetch(`/api/rooms/${this.roomId}/timers/${timerId}/control`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ action, data })
            });
            
            if (!response.ok) {
                throw new Error('Failed to control timer');
            }
        } catch (error) {
            console.error('Error controlling timer:', error);
            alert('Error controlling timer. Please try again.');
        }
    }
    
    async addTime(timerId, seconds) {
        await this.controlTimer(timerId, 'add_time', { seconds });
    }
    
    async createTimer() {
        const title = document.getElementById('timerTitle').value;
        const duration = parseInt(document.getElementById('timerDuration').value) * 60; // Convert to seconds
        const timerType = document.getElementById('timerType').value;
        const wrapUpYellow = parseInt(document.getElementById('wrapUpYellow').value);
        const wrapUpRed = parseInt(document.getElementById('wrapUpRed').value);
        
        if (!title || duration <= 0) {
            alert('Please fill in all required fields.');
            return;
        }
        
        try {
            const response = await fetch(`/api/rooms/${this.roomId}/timers`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    title,
                    duration: duration.toString(),
                    timer_type: timerType,
                    wrap_up_yellow: wrapUpYellow.toString(),
                    wrap_up_red: wrapUpRed.toString()
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                this.timers.set(data.timer_id, data.timer);
                this.updateTimersGrid();
                this.closeModal('createTimerModal');
                
                // Clear form
                document.getElementById('timerTitle').value = '';
                document.getElementById('timerDuration').value = '5';
                document.getElementById('timerType').value = 'countdown';
                document.getElementById('wrapUpYellow').value = '60';
                document.getElementById('wrapUpRed').value = '30';
            } else {
                throw new Error('Failed to create timer');
            }
        } catch (error) {
            console.error('Error creating timer:', error);
            alert('Error creating timer. Please try again.');
        }
    }
    
    async sendMessage() {
        const content = document.getElementById('messageContent').value;
        const color = document.getElementById('messageColor').value;
        const isBold = document.getElementById('messageBold').checked;
        const isUppercase = document.getElementById('messageUppercase').checked;
        const isFlashing = document.getElementById('messageFlashing').checked;
        
        if (!content.trim()) {
            alert('Please enter a message.');
            return;
        }
        
        try {
            const response = await fetch(`/api/rooms/${this.roomId}/messages`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    content: content.trim(),
                    color,
                    is_bold: isBold.toString(),
                    is_uppercase: isUppercase.toString(),
                    is_flashing: isFlashing.toString()
                })
            });
            
            if (response.ok) {
                document.getElementById('messageContent').value = '';
                alert('Message sent successfully!');
            } else {
                throw new Error('Failed to send message');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            alert('Error sending message. Please try again.');
        }
    }
    
    async sendQuickMessage(content, color = '#ffffff') {
        document.getElementById('messageContent').value = content;
        document.getElementById('messageColor').value = color;
        await this.sendMessage();
    }
    
    async refreshDevices() {
        await this.loadDevices();
    }
}

// Global functions for HTML onclick handlers
function startAllTimers() {
    controller.timers.forEach(timer => {
        if (timer.state !== 'running') {
            controller.controlTimer(timer.id, 'start');
        }
    });
}

function stopAllTimers() {
    controller.timers.forEach(timer => {
        if (timer.state === 'running') {
            controller.controlTimer(timer.id, 'stop');
        }
    });
}

function resetAllTimers() {
    controller.timers.forEach(timer => {
        controller.controlTimer(timer.id, 'reset');
    });
}

function addTimeToAll(seconds) {
    controller.timers.forEach(timer => {
        controller.addTime(timer.id, seconds);
    });
}

function createTimer() {
    controller.createTimer();
}

function closeModal(modalId) {
    controller.closeModal(modalId);
}

function sendMessage() {
    controller.sendMessage();
}

function sendQuickMessage(content, color) {
    controller.sendQuickMessage(content, color);
}

function refreshDevices() {
    controller.refreshDevices();
}

// Initialize controller when page loads
let controller;
document.addEventListener('DOMContentLoaded', () => {
    controller = new Controller();
}); 