// CueSync - AI-Powered Presentation Timer
// Enhanced JavaScript for Flask backend integration

class CueSyncApp {
    constructor() {
        this.currentPage = 'landing';
        this.roomId = null;
        this.isController = false;
        this.timers = [];
        this.messages = [];
        this.agenda = [];
        this.activeTimerId = null;
        this.currentTimerInterval = null;
        this.settings = {
            theme: 'default',
            sounds_enabled: true,
            auto_advance: true,
            ai_suggestions: true,
            voice_control: true,
            voice_feedback: true
        };
        this.connectedViewers = 0;
        this.socket = null;
        this.aiInsights = {};
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initSocketConnection();
        this.showPage('landing');
    }

    initSocketConnection() {
        // Initialize Socket.IO connection
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('Connected to CueSync server');
            this.updateAIStatus('Connected to AI server');
        });
        
        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
            this.updateAIStatus('Disconnected from AI server');
        });
        
        this.socket.on('timer_created', (timer) => {
            this.handleTimerCreated(timer);
        });
        
        this.socket.on('timer_started', (data) => {
            this.handleTimerStarted(data);
        });
        
        this.socket.on('timer_updated', (data) => {
            this.handleTimerUpdated(data);
        });
        
        this.socket.on('message_sent', (message) => {
            this.handleMessageReceived(message);
        });
        
        this.socket.on('voice_command_processed', (data) => {
            this.handleVoiceCommandProcessed(data);
        });
        
        this.socket.on('ai_insights_updated', (insights) => {
            this.handleAIInsightsUpdated(insights);
        });
        
        this.socket.on('viewer_count_updated', (data) => {
            this.updateViewerCount(data.count);
        });
    }

    setupEventListeners() {
        // Landing page
        document.getElementById('create-room-btn').addEventListener('click', () => this.createRoom());
        document.getElementById('join-room-btn').addEventListener('click', () => this.joinRoom());
        document.getElementById('room-id-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.joinRoom();
        });

        // Controller
        document.getElementById('copy-link-btn').addEventListener('click', () => this.copyViewerLink());
        document.getElementById('voice-control-btn').addEventListener('click', () => this.toggleVoiceControl());
        document.getElementById('ai-suggestions-btn').addEventListener('click', () => this.getAISuggestions());
        document.getElementById('settings-btn').addEventListener('click', () => this.openSettings());
        document.getElementById('ai-settings-btn').addEventListener('click', () => this.openAISettings());
        document.getElementById('fullscreen-viewer-btn').addEventListener('click', () => this.openViewer());
        document.getElementById('add-timer-btn').addEventListener('click', () => this.openAddTimerModal());
        document.getElementById('send-message-btn').addEventListener('click', () => this.sendMessage());
        document.getElementById('analyze-content-btn').addEventListener('click', () => this.analyzeContent());
        document.getElementById('import-csv-btn').addEventListener('click', () => this.importCSV());
        document.getElementById('clear-agenda-btn').addEventListener('click', () => this.clearAgenda());

        // Viewer
        document.getElementById('back-to-controller-btn').addEventListener('click', () => this.backToController());

        // Add Timer Modal
        document.getElementById('close-add-timer-modal').addEventListener('click', () => this.closeAddTimerModal());
        document.getElementById('cancel-add-timer').addEventListener('click', () => this.closeAddTimerModal());
        document.getElementById('confirm-add-timer').addEventListener('click', () => this.addTimer());
        document.getElementById('add-timer-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addTimer();
        });

        // AI Settings Modal
        document.getElementById('close-ai-settings-modal').addEventListener('click', () => this.closeAISettings());
        document.getElementById('cancel-ai-settings').addEventListener('click', () => this.closeAISettings());
        document.getElementById('save-ai-settings').addEventListener('click', () => this.saveAISettings());
        document.getElementById('test-voice-btn').addEventListener('click', () => this.testVoice());

        // Settings Modal
        document.getElementById('close-settings-modal').addEventListener('click', () => this.closeSettings());
        document.getElementById('cancel-settings').addEventListener('click', () => this.closeSettings());
        document.getElementById('save-settings').addEventListener('click', () => this.saveSettings());

        // CSV Import
        document.getElementById('csv-import').addEventListener('change', (e) => this.handleCSVImport(e));

        // Message input
        document.getElementById('message-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));

        // Modal click outside to close
        document.querySelectorAll('.modal-overlay').forEach(overlay => {
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) {
                    overlay.classList.remove('active');
                }
            });
        });
    }

    // Page Management
    showPage(page) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(`${page}-page`).classList.add('active');
        this.currentPage = page;

        if (page === 'controller') {
            this.updateControllerInterface();
        } else if (page === 'viewer') {
            this.updateViewerInterface();
        }
    }

    // Room Management
    async createRoom() {
        try {
            const response = await fetch('/api/rooms', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.roomId = data.room_id;
                this.timers = data.timers;
                this.isController = true;
                
                // Join room via socket
                this.socket.emit('join', { room_id: this.roomId });
                
                this.showToast('Room created successfully!', 'success');
                this.showPage('controller');
                this.updateAIStatus('Room created with AI-powered timers');
            } else {
                this.showToast('Failed to create room', 'error');
            }
        } catch (error) {
            console.error('Error creating room:', error);
            this.showToast('Error creating room', 'error');
        }
    }

    async joinRoom() {
        const input = document.getElementById('room-id-input');
        const roomId = input.value.trim().toUpperCase();
        
        if (!roomId) {
            this.showToast('Please enter a room ID', 'error');
            return;
        }

        if (roomId.length !== 8) {
            this.showToast('Room ID must be 8 characters', 'error');
            return;
        }

        try {
            const response = await fetch(`/api/rooms/${roomId}`);
            const data = await response.json();
            
            if (data.success) {
                this.roomId = roomId;
                this.timers = data.room.timers;
                this.messages = data.room.messages;
                this.agenda = data.room.agenda;
                this.settings = data.room.settings;
                this.aiInsights = data.room.ai_insights;
                this.isController = false;
                
                // Join room via socket
                this.socket.emit('join', { room_id: this.roomId });
                
                this.showToast('Joined room successfully!', 'success');
                this.showPage('viewer');
                this.updateAIStatus('Connected to presentation room');
            } else {
                this.showToast('Room not found', 'error');
            }
        } catch (error) {
            console.error('Error joining room:', error);
            this.showToast('Error joining room', 'error');
        }
    }

    openViewer() {
        this.showPage('viewer');
    }

    backToController() {
        if (this.isController) {
            this.showPage('controller');
        } else {
            this.showToast('You are not the controller of this room', 'error');
        }
    }

    copyViewerLink() {
        const link = `${window.location.origin}/?room=${this.roomId}&mode=viewer`;
        navigator.clipboard.writeText(link).then(() => {
            this.showToast('Viewer link copied to clipboard!', 'success');
        }).catch(() => {
            this.showToast(`Viewer link: ${link}`, 'info');
        });
    }

    // Timer Management
    async addTimer() {
        const name = document.getElementById('timer-name-input').value.trim();
        const durationInput = document.getElementById('timer-duration-input').value.trim();
        const type = document.getElementById('timer-type-select').value;
        
        if (!name || !durationInput) {
            this.showToast('Please fill in all required fields', 'error');
            return;
        }

        const duration = this.parseDuration(durationInput);
        if (duration === null) {
            this.showToast('Invalid duration format. Use MM:SS, H:MM:SS, or seconds', 'error');
            return;
        }

        const warningTimes = [];
        document.querySelectorAll('.warning-checkboxes input:checked').forEach(checkbox => {
            warningTimes.push(parseInt(checkbox.value));
        });

        const timerData = {
            name: name,
            duration: duration,
            type: type,
            warning_times: warningTimes
        };

        try {
            const response = await fetch('/api/timers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    room_id: this.roomId,
                    timer: timerData
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.timers.push(data.timer);
                this.closeAddTimerModal();
                this.showToast('Timer created with AI assistance!', 'success');
                this.updateAIStatus('Timer enhanced with AI suggestions');
            } else {
                this.showToast('Failed to create timer', 'error');
            }
        } catch (error) {
            console.error('Error creating timer:', error);
            this.showToast('Error creating timer', 'error');
        }
    }

    async startTimer(timerId) {
        try {
            const response = await fetch(`/api/timers/${timerId}/start`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    room_id: this.roomId
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.activeTimerId = timerId;
                this.updateAIStatus('Timer started with AI monitoring');
                
                // Update AI insights
                if (data.ai_suggestions) {
                    this.updateAIInsights(data.ai_suggestions);
                }
            } else {
                this.showToast('Failed to start timer', 'error');
            }
        } catch (error) {
            console.error('Error starting timer:', error);
            this.showToast('Error starting timer', 'error');
        }
    }

    // AI Features
    async processVoiceCommand(commandText) {
        try {
            const response = await fetch('/api/voice-command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    room_id: this.roomId,
                    command_text: commandText
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.updateAIStatus(`Voice command processed: ${commandText}`);
                return data.ai_response;
            } else {
                this.showToast('Failed to process voice command', 'error');
                return null;
            }
        } catch (error) {
            console.error('Error processing voice command:', error);
            this.showToast('Error processing voice command', 'error');
            return null;
        }
    }

    async analyzeContent() {
        const content = document.getElementById('content-input').value.trim();
        
        if (!content) {
            this.showToast('Please enter content to analyze', 'error');
            return;
        }

        try {
            const response = await fetch('/api/analyze-content', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    room_id: this.roomId,
                    content: content
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Add suggested timers
                if (data.suggested_timers && data.suggested_timers.length > 0) {
                    this.timers.push(...data.suggested_timers);
                    this.showToast(`AI suggested ${data.suggested_timers.length} timers!`, 'success');
                }
                
                // Update AI insights
                this.updateAIInsights(data.analysis);
                this.updateAIStatus('Content analyzed with AI');
            } else {
                this.showToast('Failed to analyze content', 'error');
            }
        } catch (error) {
            console.error('Error analyzing content:', error);
            this.showToast('Error analyzing content', 'error');
        }
    }

    async getAISuggestions() {
        try {
            const response = await fetch(`/api/suggestions?room_id=${this.roomId}`);
            const data = await response.json();
            
            if (data.success) {
                this.updateAISuggestions(data.suggestions);
                this.updateAIStatus('AI suggestions updated');
            } else {
                this.showToast('Failed to get AI suggestions', 'error');
            }
        } catch (error) {
            console.error('Error getting AI suggestions:', error);
            this.showToast('Error getting AI suggestions', 'error');
        }
    }

    // Message Management
    async sendMessage() {
        const text = document.getElementById('message-input').value.trim();
        const type = document.getElementById('message-type').value;
        const flash = document.getElementById('message-flash').checked;
        
        if (!text) {
            this.showToast('Please enter a message', 'error');
            return;
        }

        const messageData = {
            text: text,
            type: type,
            flash: flash
        };

        try {
            const response = await fetch('/api/messages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    room_id: this.roomId,
                    message: messageData
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                document.getElementById('message-input').value = '';
                this.showToast('Message sent with AI enhancement!', 'success');
            } else {
                this.showToast('Failed to send message', 'error');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.showToast('Error sending message', 'error');
        }
    }

    // UI Updates
    updateControllerInterface() {
        this.renderTimerList();
        this.updateTimerDisplays();
        this.renderMessageHistory();
        this.renderAgenda();
        this.updateAIInsights(this.aiInsights);
    }

    updateViewerInterface() {
        this.updateTimerDisplays();
        this.updateAgendaProgress();
    }

    updateTimerDisplays() {
        const activeTimer = this.timers.find(t => t.id === this.activeTimerId);
        
        if (activeTimer) {
            const timeDisplay = this.formatTime(activeTimer.current_time || activeTimer.duration);
            
            // Update preview
            document.getElementById('preview-timer-name').textContent = activeTimer.name;
            document.getElementById('preview-timer-time').textContent = timeDisplay;
            document.getElementById('preview-timer-status').textContent = activeTimer.state || 'stopped';
            
            // Update viewer
            document.getElementById('viewer-timer-name').textContent = activeTimer.name;
            document.getElementById('viewer-timer-time').textContent = timeDisplay;
            
            // Update timer list
            this.renderTimerList();
        }
    }

    renderTimerList() {
        const timerList = document.getElementById('timer-list');
        timerList.innerHTML = '';
        
        this.timers.forEach(timer => {
            const timerItem = document.createElement('div');
            timerItem.className = `timer-item ${timer.id === this.activeTimerId ? 'active' : ''}`;
            timerItem.innerHTML = `
                <div class="timer-header">
                    <div class="timer-name">${timer.name}</div>
                    <div class="timer-state ${timer.state || 'stopped'}">${timer.state || 'stopped'}</div>
                </div>
                <div class="timer-time-display">${this.formatTime(timer.current_time || timer.duration)}</div>
                <div class="timer-controls">
                    <button class="btn btn--sm" onclick="app.startTimer('${timer.id}')">Start</button>
                    <button class="btn btn--sm" onclick="app.pauseTimer('${timer.id}')">Pause</button>
                    <button class="btn btn--sm" onclick="app.resetTimer('${timer.id}')">Reset</button>
                </div>
            `;
            timerList.appendChild(timerItem);
        });
    }

    updateAIInsights(insights) {
        this.aiInsights = insights;
        
        const insightsContent = document.getElementById('ai-insights-content');
        if (insightsContent) {
            let html = '';
            
            if (insights.speaking_pace) {
                html += `<p><strong>Speaking Pace:</strong> ${insights.speaking_pace}</p>`;
            }
            if (insights.audience_engagement) {
                html += `<p><strong>Engagement:</strong> ${insights.audience_engagement}</p>`;
            }
            if (insights.suggestions) {
                html += `<p><strong>Suggestions:</strong> ${insights.suggestions.join(', ')}</p>`;
            }
            
            insightsContent.innerHTML = html || '<p>AI insights will appear here...</p>';
        }
        
        // Update viewer insights
        if (insights.speaking_pace) {
            document.getElementById('speaking-pace-value').textContent = insights.speaking_pace;
        }
        if (insights.audience_engagement) {
            document.getElementById('engagement-value').textContent = insights.audience_engagement;
        }
    }

    updateAISuggestions(suggestions) {
        const suggestionsContent = document.getElementById('ai-suggestions-content');
        if (suggestionsContent) {
            let html = '';
            
            if (suggestions.timing) {
                html += `<p><strong>Timing:</strong> ${suggestions.timing}</p>`;
            }
            if (suggestions.pace) {
                html += `<p><strong>Pace:</strong> ${suggestions.pace}</p>`;
            }
            if (suggestions.engagement) {
                html += `<p><strong>Engagement:</strong> ${suggestions.engagement}</p>`;
            }
            
            suggestionsContent.innerHTML = html || '<p>AI suggestions will appear here...</p>';
        }
    }

    updateAIStatus(status) {
        const statusText = document.getElementById('ai-status-text');
        if (statusText) {
            statusText.textContent = status;
        }
    }

    updateViewerCount(count) {
        this.connectedViewers = count;
        const viewerCount = document.getElementById('viewer-count');
        if (viewerCount) {
            viewerCount.textContent = `${count} viewers connected`;
        }
    }

    // Utility Functions
    formatTime(seconds) {
        if (seconds < 0) seconds = 0;
        
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        if (hours > 0) {
            return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        } else {
            return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
    }

    parseDuration(input) {
        try {
            if (input.includes(':')) {
                const parts = input.split(':');
                if (parts.length === 2) { // MM:SS
                    const minutes = parseInt(parts[0]);
                    const seconds = parseInt(parts[1]);
                    return minutes * 60 + seconds;
                } else if (parts.length === 3) { // HH:MM:SS
                    const hours = parseInt(parts[0]);
                    const minutes = parseInt(parts[1]);
                    const seconds = parseInt(parts[2]);
                    return hours * 3600 + minutes * 60 + seconds;
                }
            } else {
                return parseInt(input);
            }
        } catch (e) {
            return null;
        }
        return null;
    }

    showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('exit');
            setTimeout(() => {
                container.removeChild(toast);
            }, 300);
        }, 3000);
    }

    // Modal Management
    openAddTimerModal() {
        document.getElementById('add-timer-modal').classList.add('active');
    }

    closeAddTimerModal() {
        document.getElementById('add-timer-modal').classList.remove('active');
        document.getElementById('add-timer-form').reset();
    }

    openAISettings() {
        document.getElementById('ai-settings-modal').classList.add('active');
    }

    closeAISettings() {
        document.getElementById('ai-settings-modal').classList.remove('active');
    }

    openSettings() {
        document.getElementById('settings-modal').classList.add('active');
    }

    closeSettings() {
        document.getElementById('settings-modal').classList.remove('active');
    }

    // AI Settings
    saveAISettings() {
        const voiceControl = document.getElementById('voice-control-enabled').checked;
        const aiSuggestions = document.getElementById('ai-suggestions-enabled').checked;
        const voiceFeedback = document.getElementById('voice-feedback-enabled').checked;
        const aiMonitoring = document.getElementById('ai-monitoring-enabled').checked;
        const voiceSpeed = document.getElementById('voice-speed-select').value;
        
        this.settings.voice_control = voiceControl;
        this.settings.ai_suggestions = aiSuggestions;
        this.settings.voice_feedback = voiceFeedback;
        this.settings.ai_monitoring = aiMonitoring;
        this.settings.voice_speed = voiceSpeed;
        
        this.closeAISettings();
        this.showToast('AI settings saved!', 'success');
    }

    saveSettings() {
        const theme = document.getElementById('theme-select').value;
        const sounds = document.getElementById('sounds-enabled').checked;
        const autoAdvance = document.getElementById('auto-advance').checked;
        
        this.settings.theme = theme;
        this.settings.sounds_enabled = sounds;
        this.settings.auto_advance = autoAdvance;
        
        this.closeSettings();
        this.showToast('Settings saved!', 'success');
    }

    toggleVoiceControl() {
        const button = document.getElementById('voice-control-btn');
        const indicator = document.getElementById('voice-control-indicator');
        
        if (this.settings.voice_control) {
            this.settings.voice_control = false;
            button.textContent = '🎤 Voice Control (Off)';
            indicator.style.display = 'none';
            this.showToast('Voice control disabled', 'info');
        } else {
            this.settings.voice_control = true;
            button.textContent = '🎤 Voice Control (On)';
            indicator.style.display = 'block';
            this.showToast('Voice control enabled', 'success');
        }
    }

    testVoice() {
        this.showToast('Testing voice functionality...', 'info');
        // Voice test would be implemented here
    }

    // Event Handlers
    handleTimerCreated(timer) {
        this.timers.push(timer);
        this.renderTimerList();
        this.showToast(`Timer "${timer.name}" created with AI assistance!`, 'success');
    }

    handleTimerStarted(data) {
        this.activeTimerId = data.timer_id;
        this.updateTimerDisplays();
        
        if (data.ai_suggestions) {
            this.updateAIInsights(data.ai_suggestions);
        }
        
        this.showToast('Timer started with AI monitoring', 'success');
    }

    handleTimerUpdated(data) {
        const timer = data.timer;
        const timerIndex = this.timers.findIndex(t => t.id === timer.id);
        
        if (timerIndex !== -1) {
            this.timers[timerIndex] = timer;
            this.updateTimerDisplays();
        }
        
        if (data.ai_insights) {
            this.updateAIInsights(data.ai_insights);
        }
    }

    handleMessageReceived(message) {
        this.messages.push(message);
        this.renderMessageHistory();
        
        if (message.flash) {
            this.displayFlashMessage(message);
        }
    }

    handleVoiceCommandProcessed(data) {
        this.showToast(`Voice command: "${data.command}"`, 'info');
        
        if (data.response && data.response.suggested_response) {
            this.showToast(data.response.suggested_response, 'success');
        }
    }

    handleAIInsightsUpdated(insights) {
        this.updateAIInsights(insights);
        this.showToast('AI insights updated', 'info');
    }

    // Additional UI Methods
    renderMessageHistory() {
        const history = document.getElementById('message-history');
        if (!history) return;
        
        history.innerHTML = '';
        
        this.messages.slice(-10).forEach(message => {
            const messageItem = document.createElement('div');
            messageItem.className = `message-item ${message.type}`;
            messageItem.innerHTML = `
                <div class="message-type ${message.type}">${message.type}</div>
                <div class="message-text">${message.text}</div>
                <div class="message-timestamp">${this.formatTimestamp(new Date(message.timestamp))}</div>
            `;
            history.appendChild(messageItem);
        });
    }

    renderAgenda() {
        const agendaList = document.getElementById('agenda-list');
        if (!agendaList) return;
        
        agendaList.innerHTML = '';
        
        this.agenda.forEach((item, index) => {
            const agendaItem = document.createElement('div');
            agendaItem.className = 'agenda-item';
            agendaItem.innerHTML = `
                <div class="agenda-title">${item.title}</div>
                <div class="agenda-duration">${this.formatTime(item.duration)}</div>
                <div class="agenda-description">${item.description}</div>
            `;
            agendaList.appendChild(agendaItem);
        });
    }

    displayFlashMessage(message) {
        const overlay = document.getElementById('preview-message-overlay');
        const content = document.getElementById('preview-message-content');
        
        if (overlay && content) {
            content.textContent = message.text;
            content.className = `message-content ${message.type}`;
            overlay.className = `message-overlay ${message.type} flash`;
            overlay.style.display = 'block';
            
            setTimeout(() => {
                overlay.style.display = 'none';
            }, 3000);
        }
    }

    formatTimestamp(date) {
        return date.toLocaleTimeString();
    }

    handleKeyboardShortcuts(event) {
        if (event.ctrlKey || event.metaKey) {
            switch (event.key) {
                case '1':
                    event.preventDefault();
                    this.showPage('landing');
                    break;
                case '2':
                    event.preventDefault();
                    if (this.isController) this.showPage('controller');
                    break;
                case '3':
                    event.preventDefault();
                    this.showPage('viewer');
                    break;
            }
        }
    }

    // CSV Import
    importCSV() {
        document.getElementById('csv-import').click();
    }

    handleCSVImport(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        const reader = new FileReader();
        reader.onload = (e) => {
            const csv = e.target.result;
            const lines = csv.split('\n');
            
            this.agenda = [];
            lines.forEach((line, index) => {
                if (index === 0) return; // Skip header
                
                const [title, duration, description] = line.split(',').map(s => s.trim());
                if (title && duration) {
                    this.agenda.push({
                        title: title,
                        duration: this.parseDuration(duration) || 300,
                        description: description || ''
                    });
                }
            });
            
            this.renderAgenda();
            this.showToast(`Imported ${this.agenda.length} agenda items`, 'success');
        };
        reader.readAsText(file);
    }

    clearAgenda() {
        this.agenda = [];
        this.renderAgenda();
        this.showToast('Agenda cleared', 'info');
    }

    updateAgendaProgress() {
        // Implementation for agenda progress tracking
    }
}

// Initialize the application
const app = new CueSyncApp(); 