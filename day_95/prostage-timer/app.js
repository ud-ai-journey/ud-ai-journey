// StageTimer Pro - Enterprise Countdown Timer Application
class StageTimerApp {
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
            auto_advance: true
        };
        this.connectedViewers = 3; // Simulated
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadSampleData();
        this.showPage('landing');
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
        document.getElementById('settings-btn').addEventListener('click', () => this.openSettings());
        document.getElementById('fullscreen-viewer-btn').addEventListener('click', () => this.openViewer());
        document.getElementById('add-timer-btn').addEventListener('click', () => this.openAddTimerModal());
        document.getElementById('send-message-btn').addEventListener('click', () => this.sendMessage());
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

    loadSampleData() {
        // Load sample data from the provided JSON
        this.timers = [
            {
                id: 'timer1',
                name: 'Opening Presentation',
                duration: 900,
                current_time: 900,
                type: 'countdown',
                state: 'stopped',
                warning_times: [120, 60, 30],
                next_timer_id: 'timer2'
            },
            {
                id: 'timer2',
                name: 'Q&A Session',
                duration: 600,
                current_time: 600,
                type: 'countdown',
                state: 'stopped',
                warning_times: [60, 30, 10],
                next_timer_id: 'timer3'
            },
            {
                id: 'timer3',
                name: 'Networking Break',
                duration: 900,
                current_time: 900,
                type: 'countdown',
                state: 'stopped',
                warning_times: [180, 60, 30],
                next_timer_id: null
            }
        ];

        this.messages = [
            {
                id: 'msg1',
                text: 'Welcome to the conference!',
                type: 'success',
                flash: false,
                timestamp: new Date('2025-07-19T15:16:30Z')
            },
            {
                id: 'msg2',
                text: 'Please prepare for Q&A',
                type: 'warning',
                flash: true,
                timestamp: new Date('2025-07-19T15:31:00Z')
            }
        ];

        this.agenda = [
            {
                title: 'Opening Presentation',
                duration: 900,
                description: 'Welcome and introduction to the conference',
                speaker: 'Dr. Smith'
            },
            {
                title: 'Q&A Session',
                duration: 600,
                description: 'Questions and answers with the audience',
                speaker: 'Dr. Smith'
            },
            {
                title: 'Networking Break',
                duration: 900,
                description: 'Coffee and networking opportunity',
                speaker: null
            }
        ];
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
    createRoom() {
        this.roomId = this.generateRoomId();
        this.isController = true;
        this.showToast('Room created successfully!', 'success');
        this.showPage('controller');
    }

    joinRoom() {
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

        this.roomId = roomId;
        this.isController = false;
        this.showToast('Joined room successfully!', 'success');
        this.showPage('viewer');
    }

    generateRoomId() {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        let result = '';
        for (let i = 0; i < 8; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
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
            // Fallback for browsers that don't support clipboard API
            this.showToast(`Viewer link: ${link}`, 'info');
        });
    }

    // Timer Management
    addTimer() {
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

        const timer = {
            id: 'timer' + Date.now(),
            name: name,
            duration: duration,
            current_time: duration,
            type: type,
            state: 'stopped',
            warning_times: warningTimes.sort((a, b) => b - a),
            next_timer_id: null
        };

        this.timers.push(timer);
        this.closeAddTimerModal();
        this.updateControllerInterface();
        this.showToast(`Timer "${name}" added successfully!`, 'success');
    }

    parseDuration(input) {
        // Handle pure seconds (e.g., "300")
        if (/^\d+$/.test(input)) {
            return parseInt(input);
        }

        // Handle MM:SS format (e.g., "5:30")
        if (/^\d{1,2}:\d{2}$/.test(input)) {
            const [minutes, seconds] = input.split(':').map(Number);
            return minutes * 60 + seconds;
        }

        // Handle H:MM:SS format (e.g., "1:30:45")
        if (/^\d{1,2}:\d{2}:\d{2}$/.test(input)) {
            const [hours, minutes, seconds] = input.split(':').map(Number);
            return hours * 3600 + minutes * 60 + seconds;
        }

        return null;
    }

    startTimer(timerId) {
        const timer = this.timers.find(t => t.id === timerId);
        if (!timer) return;

        // Stop any currently running timer
        if (this.activeTimerId && this.activeTimerId !== timerId) {
            this.pauseTimer(this.activeTimerId);
        }

        timer.state = 'running';
        this.activeTimerId = timerId;
        
        this.currentTimerInterval = setInterval(() => {
            if (timer.type === 'countdown') {
                timer.current_time--;
                if (timer.current_time <= 0) {
                    timer.current_time = 0;
                    timer.state = 'completed';
                    this.onTimerComplete(timer);
                    return;
                }
            } else {
                timer.current_time++;
            }
            
            this.updateTimerDisplays();
        }, 1000);

        this.updateTimerDisplays();
        this.showToast(`Timer "${timer.name}" started`, 'success');
    }

    pauseTimer(timerId) {
        const timer = this.timers.find(t => t.id === timerId);
        if (!timer) return;

        timer.state = 'paused';
        if (this.currentTimerInterval) {
            clearInterval(this.currentTimerInterval);
            this.currentTimerInterval = null;
        }

        this.updateTimerDisplays();
        this.showToast(`Timer "${timer.name}" paused`, 'warning');
    }

    stopTimer(timerId) {
        const timer = this.timers.find(t => t.id === timerId);
        if (!timer) return;

        timer.state = 'stopped';
        timer.current_time = timer.duration;
        
        if (this.currentTimerInterval) {
            clearInterval(this.currentTimerInterval);
            this.currentTimerInterval = null;
        }

        if (this.activeTimerId === timerId) {
            this.activeTimerId = null;
        }

        this.updateTimerDisplays();
        this.showToast(`Timer "${timer.name}" stopped`, 'info');
    }

    resetTimer(timerId) {
        const timer = this.timers.find(t => t.id === timerId);
        if (!timer) return;

        timer.current_time = timer.duration;
        if (timer.state === 'completed') {
            timer.state = 'stopped';
        }

        this.updateTimerDisplays();
        this.showToast(`Timer "${timer.name}" reset`, 'info');
    }

    deleteTimer(timerId) {
        if (confirm('Are you sure you want to delete this timer?')) {
            this.timers = this.timers.filter(t => t.id !== timerId);
            if (this.activeTimerId === timerId) {
                this.stopTimer(timerId);
            }
            this.updateControllerInterface();
            this.showToast('Timer deleted', 'success');
        }
    }

    onTimerComplete(timer) {
        if (this.currentTimerInterval) {
            clearInterval(this.currentTimerInterval);
            this.currentTimerInterval = null;
        }

        this.activeTimerId = null;
        this.showToast(`Timer "${timer.name}" completed!`, 'success');

        // Auto-advance if enabled and next timer exists
        if (this.settings.auto_advance && timer.next_timer_id) {
            setTimeout(() => {
                this.startTimer(timer.next_timer_id);
            }, 2000);
        }

        this.updateTimerDisplays();
    }

    // Display Updates
    updateControllerInterface() {
        if (this.currentPage !== 'controller') return;

        // Update room info
        document.getElementById('room-id-display').textContent = this.roomId || 'ABC123XY';
        document.getElementById('viewer-count').textContent = `${this.connectedViewers} viewers connected`;

        // Update timer list
        this.renderTimerList();
        
        // Update main display preview
        this.updateTimerDisplays();
        
        // Update message history
        this.renderMessageHistory();
        
        // Update agenda
        this.renderAgenda();
    }

    updateViewerInterface() {
        if (this.currentPage !== 'viewer') return;

        document.getElementById('viewer-room-id').textContent = this.roomId || 'ABC123XY';
        
        const activeTimer = this.timers.find(t => t.id === this.activeTimerId);
        const timerDisplay = document.getElementById('viewer-timer-display');
        const timerName = document.getElementById('viewer-timer-name');
        const timerTime = document.getElementById('viewer-timer-time');
        
        if (activeTimer) {
            timerName.textContent = activeTimer.name;
            timerTime.textContent = this.formatTime(activeTimer.current_time);
            
            // Apply warning styles
            timerDisplay.className = 'viewer-timer-display';
            if (activeTimer.type === 'countdown') {
                if (activeTimer.current_time <= 0) {
                    timerDisplay.classList.add('expired');
                } else if (activeTimer.warning_times.some(w => activeTimer.current_time <= w)) {
                    timerDisplay.classList.add('warning');
                }
            }
        } else {
            timerName.textContent = 'Waiting for timer...';
            timerTime.textContent = '--:--';
            timerDisplay.className = 'viewer-timer-display';
        }

        // Update agenda progress
        this.updateAgendaProgress();
    }

    updateTimerDisplays() {
        const activeTimer = this.timers.find(t => t.id === this.activeTimerId);
        
        // Update controller preview
        const previewName = document.getElementById('preview-timer-name');
        const previewTime = document.getElementById('preview-timer-time');
        const previewStatus = document.getElementById('preview-timer-status');
        const previewDisplay = document.getElementById('main-timer-display');
        
        if (activeTimer) {
            previewName.textContent = activeTimer.name;
            previewTime.textContent = this.formatTime(activeTimer.current_time);
            previewStatus.textContent = activeTimer.state.charAt(0).toUpperCase() + activeTimer.state.slice(1);
            
            // Apply warning styles
            previewDisplay.className = 'timer-display';
            if (activeTimer.type === 'countdown') {
                if (activeTimer.current_time <= 0) {
                    previewDisplay.classList.add('expired');
                } else if (activeTimer.warning_times.some(w => activeTimer.current_time <= w)) {
                    previewDisplay.classList.add('warning');
                }
            }
        } else {
            previewName.textContent = 'Select a timer';
            previewTime.textContent = '--:--';
            previewStatus.textContent = 'No active timer';
            previewDisplay.className = 'timer-display';
        }
        
        // Update timer list states
        this.renderTimerList();
        
        // Update viewer if on viewer page
        if (this.currentPage === 'viewer') {
            this.updateViewerInterface();
        }
    }

    renderTimerList() {
        const container = document.getElementById('timer-list');
        if (!container) return;

        if (this.timers.length === 0) {
            container.innerHTML = '<div style="text-align: center; color: var(--color-text-secondary); padding: var(--space-16);">No timers added yet. Click "Add Timer" to get started.</div>';
            return;
        }

        container.innerHTML = this.timers.map(timer => {
            const isActive = timer.id === this.activeTimerId;
            const isRunning = timer.state === 'running';
            
            return `
                <div class="timer-item ${timer.state} ${isActive ? 'active' : ''}" data-timer-id="${timer.id}">
                    <div class="timer-header">
                        <div class="timer-name">${timer.name}</div>
                        <div class="timer-state ${timer.state}">${timer.state}</div>
                    </div>
                    <div class="timer-time-display">${this.formatTime(timer.current_time)}</div>
                    <div class="timer-controls">
                        ${isRunning ? 
                            `<button class="btn btn--secondary btn--sm" onclick="window.app.pauseTimer('${timer.id}')" title="Pause">⏸️</button>` :
                            `<button class="btn btn--primary btn--sm" onclick="window.app.startTimer('${timer.id}')" title="Start">▶️</button>`
                        }
                        <button class="btn btn--outline btn--sm" onclick="window.app.stopTimer('${timer.id}')" title="Stop">⏹️</button>
                        <button class="btn btn--outline btn--sm" onclick="window.app.resetTimer('${timer.id}')" title="Reset">🔄</button>
                        <button class="btn btn--outline btn--sm" onclick="window.app.deleteTimer('${timer.id}')" title="Delete">🗑️</button>
                    </div>
                </div>
            `;
        }).join('');
    }

    formatTime(seconds) {
        if (seconds < 0) seconds = 0;
        
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        if (hours > 0) {
            return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        } else {
            return `${minutes}:${secs.toString().padStart(2, '0')}`;
        }
    }

    // Message System
    sendMessage() {
        const input = document.getElementById('message-input');
        const typeSelect = document.getElementById('message-type');
        const flashCheck = document.getElementById('message-flash');
        
        const text = input.value.trim();
        if (!text) {
            this.showToast('Please enter a message', 'error');
            return;
        }

        const message = {
            id: 'msg' + Date.now(),
            text: text,
            type: typeSelect.value,
            flash: flashCheck.checked,
            timestamp: new Date()
        };

        this.messages.unshift(message);
        this.displayMessage(message);
        this.renderMessageHistory();
        
        // Clear form
        input.value = '';
        flashCheck.checked = false;
        
        this.showToast('Message sent!', 'success');
    }

    displayMessage(message) {
        // Show on controller preview
        const previewOverlay = document.getElementById('preview-message-overlay');
        const previewContent = document.getElementById('preview-message-content');
        
        if (previewOverlay && previewContent) {
            previewOverlay.className = `message-overlay ${message.type} ${message.flash ? 'flash' : ''}`;
            previewContent.textContent = message.text;
            previewOverlay.style.display = 'block';
        }
        
        // Show on viewer if on viewer page
        if (this.currentPage === 'viewer') {
            const viewerOverlay = document.getElementById('viewer-message-overlay');
            const viewerContent = document.getElementById('viewer-message-content');
            
            if (viewerOverlay && viewerContent) {
                viewerOverlay.className = `viewer-message-overlay ${message.type} ${message.flash ? 'flash' : ''}`;
                viewerContent.textContent = message.text;
                viewerOverlay.style.display = 'block';
            }
        }

        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (previewOverlay) previewOverlay.style.display = 'none';
            const viewerOverlay = document.getElementById('viewer-message-overlay');
            if (viewerOverlay) viewerOverlay.style.display = 'none';
        }, 5000);
    }

    renderMessageHistory() {
        const container = document.getElementById('message-history');
        if (!container) return;

        if (this.messages.length === 0) {
            container.innerHTML = '<div style="text-align: center; color: var(--color-text-secondary); padding: var(--space-16);">No messages sent yet.</div>';
            return;
        }

        container.innerHTML = this.messages.slice(0, 10).map(message => `
            <div class="message-item">
                <div class="message-type ${message.type}">${message.type}</div>
                <div class="message-text">${message.text}</div>
                <div class="message-timestamp">${this.formatTimestamp(message.timestamp)}</div>
            </div>
        `).join('');
    }

    formatTimestamp(date) {
        return date.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }

    // Agenda Management
    renderAgenda() {
        const container = document.getElementById('agenda-list');
        if (!container) return;

        if (this.agenda.length === 0) {
            container.innerHTML = '<div style="text-align: center; color: var(--color-text-secondary); padding: var(--space-16);">No agenda items. Import CSV or add items manually.</div>';
            return;
        }

        container.innerHTML = this.agenda.map((item, index) => `
            <div class="agenda-item ${index === 0 ? 'current' : index <= 2 ? 'upcoming' : ''}" draggable="true">
                <div class="agenda-title">${item.title}</div>
                <div class="agenda-duration">${this.formatTime(item.duration)}</div>
                <div class="agenda-description">${item.description}</div>
                ${item.speaker ? `<div class="agenda-speaker">Speaker: ${item.speaker}</div>` : ''}
            </div>
        `).join('');
    }

    updateAgendaProgress() {
        const progressFill = document.querySelector('#viewer-agenda-progress .progress-fill');
        const currentItem = document.getElementById('viewer-current-agenda');
        
        if (this.agenda.length > 0) {
            const progress = Math.min(100, (1 / this.agenda.length) * 100);
            if (progressFill) progressFill.style.width = `${progress}%`;
            if (currentItem) currentItem.textContent = this.agenda[0].title;
        }
    }

    importCSV() {
        const fileInput = document.getElementById('csv-import');
        if (fileInput) {
            fileInput.click();
        } else {
            this.showToast('CSV import not available', 'error');
        }
    }

    handleCSVImport(event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const csv = e.target.result;
                const lines = csv.split('\n').filter(line => line.trim());
                
                if (lines.length < 2) {
                    this.showToast('CSV file must have at least a header and one data row', 'error');
                    return;
                }
                
                const newAgenda = [];
                for (let i = 1; i < lines.length; i++) {
                    const values = lines[i].split(',').map(v => v.trim().replace(/"/g, ''));
                    if (values.length >= 2 && values[0]) {
                        const item = {
                            title: values[0] || `Item ${i}`,
                            duration: this.parseDuration(values[1]) || 300,
                            description: values[2] || '',
                            speaker: values[3] || null
                        };
                        newAgenda.push(item);
                    }
                }
                
                if (newAgenda.length > 0) {
                    this.agenda = newAgenda;
                    this.renderAgenda();
                    this.showToast(`Imported ${newAgenda.length} agenda items`, 'success');
                } else {
                    this.showToast('No valid agenda items found in CSV', 'error');
                }
            } catch (error) {
                console.error('CSV Import Error:', error);
                this.showToast('Error parsing CSV file', 'error');
            }
        };
        
        reader.onerror = () => {
            this.showToast('Error reading file', 'error');
        };
        
        reader.readAsText(file);
        
        // Reset file input
        event.target.value = '';
    }

    clearAgenda() {
        if (confirm('Are you sure you want to clear the agenda?')) {
            this.agenda = [];
            this.renderAgenda();
            this.showToast('Agenda cleared', 'success');
        }
    }

    // Modal Management
    openAddTimerModal() {
        document.getElementById('add-timer-modal').classList.add('active');
        document.getElementById('timer-name-input').focus();
    }

    closeAddTimerModal() {
        document.getElementById('add-timer-modal').classList.remove('active');
        document.getElementById('add-timer-form').reset();
    }

    openSettings() {
        document.getElementById('settings-modal').classList.add('active');
        
        // Load current settings
        document.getElementById('theme-select').value = this.settings.theme;
        document.getElementById('sounds-enabled').checked = this.settings.sounds_enabled;
        document.getElementById('auto-advance').checked = this.settings.auto_advance;
    }

    closeSettings() {
        document.getElementById('settings-modal').classList.remove('active');
    }

    saveSettings() {
        this.settings.theme = document.getElementById('theme-select').value;
        this.settings.sounds_enabled = document.getElementById('sounds-enabled').checked;
        this.settings.auto_advance = document.getElementById('auto-advance').checked;
        
        // Apply theme
        document.body.setAttribute('data-theme', this.settings.theme);
        
        this.closeSettings();
        this.showToast('Settings saved!', 'success');
    }

    // Keyboard Shortcuts
    handleKeyboardShortcuts(event) {
        if (this.currentPage !== 'controller') return;
        
        // Ignore if typing in input fields
        if (event.target.matches('input, textarea, select')) return;

        switch (event.code) {
            case 'Space':
                event.preventDefault();
                if (this.activeTimerId) {
                    const activeTimer = this.timers.find(t => t.id === this.activeTimerId);
                    if (activeTimer.state === 'running') {
                        this.pauseTimer(this.activeTimerId);
                    } else {
                        this.startTimer(this.activeTimerId);
                    }
                } else if (this.timers.length > 0) {
                    // Start first timer if no active timer
                    this.startTimer(this.timers[0].id);
                }
                break;
            case 'KeyS':
                if (event.ctrlKey || event.metaKey) {
                    event.preventDefault();
                    if (this.activeTimerId) {
                        this.stopTimer(this.activeTimerId);
                    }
                }
                break;
            case 'KeyR':
                if (event.ctrlKey || event.metaKey) {
                    event.preventDefault();
                    if (this.activeTimerId) {
                        this.resetTimer(this.activeTimerId);
                    }
                }
                break;
        }
    }

    // Toast Notifications
    showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;
        
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        container.appendChild(toast);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            toast.classList.add('exit');
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 3000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new StageTimerApp();
    
    // Check URL parameters for direct room joining
    const urlParams = new URLSearchParams(window.location.search);
    const roomId = urlParams.get('room');
    const mode = urlParams.get('mode');
    
    if (roomId) {
        app.roomId = roomId;
        if (mode === 'viewer') {
            app.isController = false;
            app.showPage('viewer');
        } else {
            app.isController = true;
            app.showPage('controller');
        }
    }
});