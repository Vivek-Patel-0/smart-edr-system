# 🛡️ Smart EDR System

A complete Endpoint Detection and Response (EDR) system with AI-powered threat detection!

## 🎯 What Does This Do?

This EDR system is like having a smart security guard for your computer that:
- 👁️ Watches files, processes, and network connections
- 🧠 Uses AI to detect suspicious behavior  
- 🚨 Sends alerts when threats are found
- 📊 Provides a beautiful web dashboard to see everything
- 💾 Stores all security events in a database

## 🚀 Quick Start

### 1. Setup
```bash
# Install dependencies
python scripts/install_requirements.py

# Create config file (optional - will use defaults)
cp config.yaml.example config.yaml
```

### 2. Start the EDR Agent
```bash
python scripts/start_edr.py
```

### 3. Start the Web Dashboard
```bash
# In another terminal
python scripts/start_dashboard.py
```

Then open http://localhost:5000 in your browser!

## 📁 Project Structure

```
smart-edr-system/
├── src/                    # Main source code
│   ├── main.py            # Application entry point
│   ├── core/              # Core EDR functionality
│   ├── monitors/          # File, process, network monitoring
│   ├── ai/                # AI threat detection
│   ├── database/          # Data storage
│   ├── api/               # Web dashboard API
│   └── utils/             # Utilities
├── scripts/               # Helper scripts
├── data/                  # Data storage
└── requirements.txt       # Python dependencies
```

## 🎮 How to Use

### Basic Usage
1. Run `python scripts/start_edr.py` to start monitoring
2. The system will watch your files and processes automatically
3. Check the logs in `data/logs/` folder
4. High-threat events will generate alerts

### Web Dashboard
1. Run `python scripts/start_dashboard.py`
2. Open http://localhost:5000
3. See real-time security events and statistics
4. Monitor threat levels and system status

### Configuration
Edit `config.yaml` to customize:
- Which folders to monitor
- Alert settings
- AI model parameters
- Database configuration

## 🧠 AI Features

The system includes:
- **Anomaly Detection**: Learns normal behavior patterns
- **Threat Scoring**: Rates events from 0-100% threat level
- **Behavioral Analysis**: Detects suspicious activity patterns
- **Adaptive Learning**: Gets smarter over time

## 🔧 Advanced Usage

### Train Custom AI Models
```bash
python src/ai/training/train_models.py
```

### Export Security Reports
```bash
python scripts/generate_report.py
```

### Custom Alert Rules
Edit the alert rules in `src/alerting/rules/rule_engine.py`

## 📊 Dashboard Features

- **Real-time Monitoring**: Live updates every 10 seconds
- **Threat Timeline**: Visual timeline of security events  
- **Statistics**: Total events, high threats, system status
- **Event Details**: Detailed information about each security event
- **Beautiful UI**: Modern, responsive design

## 🛠️ Customization

### Add New Monitors
Create new monitor classes in `src/monitors/`

### Custom AI Models
Add new AI models in `src/ai/models/`

### Alert Integrations
Add new alert methods in `src/alerting/notifications/`

## 🔍 Troubleshooting

### Common Issues
1. **Permission Errors**: Run as administrator on Windows
2. **Port 5000 Busy**: Change port in `src/api/app.py`
3. **Database Errors**: Delete `data/edr.db` to reset

### Debug Mode
Set `log_level: DEBUG` in config.yaml for verbose logging

## 📚 Learning Resources

This project teaches:
- **Python Programming**: Object-oriented design, threading, databases
- **Cybersecurity**: EDR concepts, threat detection, incident response
- **AI/ML**: Anomaly detection, behavioral analysis, pattern recognition
- **Web Development**: Flask APIs, JavaScript, responsive design
- **System Programming**: File monitoring, process management, network analysis

## 🎯 Next Steps

1. **Start Simple**: Run the basic file monitor first
2. **Add Features**: Enable process and network monitoring
3. **Train AI**: Collect data and train custom models
4. **Customize**: Add your own detection rules
5. **Scale Up**: Deploy to multiple machines

## 🤝 Contributing

This is a learning project! Feel free to:
- Add new monitoring capabilities
- Improve the AI models
- Enhance the web dashboard
- Create better alert systems

## 📄 License

This project is for educational purposes. Use responsibly!

---

**Remember**: This is like building with LEGO blocks - start with one piece at a time, and soon you'll have a complete security system! 🎉