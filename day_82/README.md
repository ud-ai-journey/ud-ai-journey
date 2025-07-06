# 🎮 SyncStage - Professional Event Timer Application - Day 82 - July 6, 2025

A professional event timer application built with Python FastAPI and modern web technologies. Perfect for managing presentations, conferences, workshops, and any event requiring precise timing control with synchronized multi-device support.

## ✨ Features

### 🎛️ **Timer Management**
- **Multiple Timer Types**: Countdown and count-up timers
- **Customizable Duration**: Set any duration in seconds
- **Warning System**: Yellow and red warning thresholds
- **Real-time Control**: Start, pause, stop, reset, and add time
- **Visual Status**: Clear indication of timer states

### 📱 **Multi-Device Support**
- **Controller Interface**: Full timer management and control
- **Viewer Interface**: Clean display for audience viewing
- **Agenda Interface**: Event schedule and participant information
- **Real-time Sync**: WebSocket communication across all devices

### 📢 **Message Broadcasting**
- **Custom Messages**: Send text messages to all viewers
- **Styling Options**: Bold, uppercase, flashing text
- **Color Customization**: Choose any color for messages
- **Instant Display**: Real-time message updates

### 🔗 **Room Management**
- **Unique Rooms**: Each event gets a unique room ID
- **Device Tracking**: Monitor connected devices
- **Secure Access**: Optional password protection
- **Persistent Sessions**: Maintain state during events

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd day_82
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser to `http://localhost:8000`
   - Create a new room or join an existing one

## 📖 Usage Guide

### Creating a Room
1. Visit `http://localhost:8000`
2. Enter a room title (e.g., "Tech Conference 2024")
3. Optionally add a password for security
4. Click "Create Room"
5. You'll receive URLs for controller, viewer, and agenda

### Managing Timers
1. **Add a Timer**:
   - Enter timer title (e.g., "Opening Speech")
   - Set duration in seconds (e.g., 300 for 5 minutes)
   - Choose timer type (countdown/count-up)
   - Set warning thresholds (yellow/red)
   - Click "Add Timer"

2. **Control Timers**:
   - **Start**: Begin the countdown
   - **Pause**: Pause the timer
   - **Stop**: Stop and reset to original duration
   - **Reset**: Reset to original duration
   - **+30s**: Add time to the timer

### Broadcasting Messages
1. Enter your message in the text field
2. Choose styling options (bold, uppercase, flashing)
3. Select a color for the message
4. Click "Send Message"
5. Message appears on all viewer screens instantly

### Multi-Device Setup
1. **Controller**: Use the main interface for timer control
2. **Viewer**: Open viewer URL in a separate tab/window for audience display
3. **Agenda**: Open agenda URL for event schedule and participant info

## 🔧 API Documentation

### REST Endpoints

#### Create Room
```http
POST /api/rooms
Content-Type: application/x-www-form-urlencoded

title=Event Title&password=optional_password
```

#### Create Timer
```http
POST /api/rooms/{room_id}/timers
Content-Type: application/json

{
  "title": "Timer Title",
  "duration": 300,
  "timer_type": "countdown",
  "wrap_up_yellow": 60,
  "wrap_up_red": 30
}
```

#### Control Timer
```http
POST /api/rooms/{room_id}/timers/{timer_id}/control
Content-Type: application/json

{
  "action": "start|pause|stop|reset|add_time",
  "data": {"seconds": 30}  // for add_time action
}
```

#### Send Message
```http
POST /api/rooms/{room_id}/messages
Content-Type: application/json

{
  "content": "Message text",
  "color": "#ffffff",
  "is_bold": false,
  "is_uppercase": false,
  "is_flashing": false
}
```

#### Get Timers
```http
GET /api/rooms/{room_id}/timers
```

#### Get Connected Devices
```http
GET /api/rooms/{room_id}/devices
```

### WebSocket Endpoint
```http
WS /ws/{room_id}?device_type=controller&device_name=Device Name
```

## 🏗️ Architecture

### Backend Components
- **FastAPI**: Modern, fast web framework
- **Timer Engine**: Core timing logic and state management
- **WebSocket Manager**: Real-time communication handler
- **Connection Manager**: Device connection tracking

### Frontend Components
- **Controller Interface**: Timer management and control
- **Viewer Interface**: Clean display for audience
- **Agenda Interface**: Event information and schedule
- **Real-time Updates**: WebSocket-driven live updates

### Data Models
- **Room**: Event container with timers and devices
- **Timer**: Individual timer with configuration and state
- **Message**: Display messages with styling options
- **ConnectedDevice**: Device tracking and management

## 🎨 Interface Features

### Controller Interface
- Timer creation and management
- Real-time timer control
- Message broadcasting
- Device connection monitoring
- Quick actions (viewer/agenda links)

### Viewer Interface
- Clean, large timer display
- Current timer status
- Warning indicators (yellow/red)
- Message display
- Responsive design

### Agenda Interface
- Event schedule display
- Participant information
- Timer status overview
- Real-time updates

## 🔍 Troubleshooting

### Common Issues

#### Timer Not Starting
- Check if the timer is properly created
- Verify WebSocket connection is active
- Ensure timer engine is running

#### Messages Not Displaying
- Check WebSocket connection status
- Verify message format is correct
- Ensure viewer page is open

#### Connection Issues
- Refresh the page
- Check if the server is running
- Verify room ID is correct

#### Performance Issues
- Close unnecessary browser tabs
- Check server resources
- Reduce number of active timers

### Debug Information
- Check browser console for JavaScript errors
- Monitor server logs for backend issues
- Verify WebSocket connection status

## 🛠️ Development

### Project Structure
```
day_82/
├── app.py                 # Main FastAPI application
├── models.py              # Data models and schemas
├── timer_engine.py        # Core timer logic
├── websocket_manager.py   # WebSocket handling
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── home.html
│   ├── controller.html
│   ├── viewer.html
│   └── agenda.html
├── static/               # Static assets
│   ├── css/
│   │   ├── common.css
│   │   ├── controller.css
│   │   ├── viewer.css
│   │   └── agenda.css
│   └── js/
│       ├── controller.js
│       ├── viewer.js
│       └── agenda.js
└── README.md            # This file
```

### Adding Features
1. **Backend**: Add new endpoints in `app.py`
2. **Frontend**: Update templates and JavaScript
3. **Styling**: Modify CSS files
4. **Testing**: Test with multiple devices

### Customization
- **Colors**: Modify CSS variables
- **Layout**: Update HTML templates
- **Functionality**: Extend timer engine
- **Messages**: Add new message types

## 📝 License

This project is created for educational and development purposes. Feel free to modify and extend for your specific needs.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Test with the provided examples
4. Create an issue with detailed information

---

**Happy Event Timing! 🎉** 