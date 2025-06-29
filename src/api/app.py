'''
Web API - Provides web interface for the EDR dashboard
Like a control panel you can access from your browser!
'''

from flask import Flask, jsonify, render_template_string, request
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from database.connection import DatabaseManager
from utils.config import load_config
from utils.logger import setup_logger

app = Flask(__name__)
config = load_config()
db_manager = DatabaseManager(config['database'])
logger = setup_logger('WebAPI')

# HTML Template for Dashboard
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Smart EDR Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .header h1 {
            color: #4a5568;
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }
        
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .stat-label {
            color: #666;
            font-size: 1.1em;
        }
        
        .events-section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        
        .section-title {
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #4a5568;
        }
        
        .event-item {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }
        
        .event-item:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .event-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .event-type {
            background: #667eea;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        
        .threat-score {
            font-weight: bold;
            padding: 5px 12px;
            border-radius: 20px;
            color: white;
        }
        
        .threat-low { background: #48bb78; }
        .threat-medium { background: #ed8936; }
        .threat-high { background: #f56565; }
        
        .event-details {
            color: #666;
            font-size: 0.95em;
        }
        
        .refresh-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }
        
        .refresh-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .loading {
            animation: pulse 2s infinite;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Smart EDR Dashboard</h1>
            <p>Real-time security monitoring and threat detection</p>
        </div>
        
        <div class="stats" id="stats">
            <div class="stat-card">
                <div class="stat-number" id="total-events">-</div>
                <div class="stat-label">Total Events</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="high-threats">-</div>
                <div class="stat-label">High Threats</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="active-monitoring">✅</div>
                <div class="stat-label">Status</div>
            </div>
        </div>
        
        <div class="events-section">
            <div class="section-title">📊 Recent Security Events</div>
            <button class="refresh-btn" onclick="refreshData()">🔄 Refresh Data</button>
            <div id="events-list" class="loading">Loading events...</div>
        </div>
    </div>

    <script>
        async function fetchData() {
            try {
                const response = await fetch('/api/dashboard');
                const data = await response.json();
                updateDashboard(data);
            } catch (error) {
                console.error('Error fetching data:', error);
                document.getElementById('events-list').innerHTML = '❌ Error loading data';
            }
        }
        
        function updateDashboard(data) {
            // Update stats
            document.getElementById('total-events').textContent = data.total_events;
            document.getElementById('high-threats').textContent = data.high_threats;
            
            // Update events list
            const eventsList = document.getElementById('events-list');
            if (data.recent_events.length === 0) {
                eventsList.innerHTML = '<p style="text-align: center; color: #666;">No recent events</p>';
                return;
            }
            
            eventsList.innerHTML = data.recent_events.map(event => {
                const threatClass = event.threat_score > 0.7 ? 'threat-high' : 
                                  event.threat_score > 0.4 ? 'threat-medium' : 'threat-low';
                
                const date = new Date(event.timestamp * 1000).toLocaleString();
                
                return `
                    <div class="event-item">
                        <div class="event-header">
                            <span class="event-type">${event.event_type}</span>
                            <span class="threat-score ${threatClass}">
                                ${(event.threat_score * 100).toFixed(0)}%
                            </span>
                        </div>
                        <div class="event-details">
                            <strong>Action:</strong> ${event.event_data.action || 'N/A'}<br>
                            <strong>Time:</strong> ${date}<br>
                            <strong>Details:</strong> ${getEventDetails(event.event_data)}
                        </div>
                    </div>
                `;
            }).join('');
        }
        
        function getEventDetails(eventData) {
            if (eventData.path) return `File: ${eventData.path}`;
            if (eventData.name) return `Process: ${eventData.name} (PID: ${eventData.pid})`;
            if (eventData.remote_addr) return `Connection: ${eventData.remote_addr.join(':')}`;
            return 'Unknown event';
        }
        
        function refreshData() {
            document.getElementById('events-list').innerHTML = '<div class="loading">Refreshing...</div>';
            fetchData();
        }
        
        // Initial load
        fetchData();
        
        // Auto-refresh every 10 seconds
        setInterval(fetchData, 10000);
    </script>
</body>
</html>
'''

@app.route('/')
def dashboard():
    '''Main dashboard page'''
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/dashboard')
def api_dashboard():
    '''API endpoint for dashboard data'''
    try:
        # Get recent events
        recent_events = db_manager.get_recent_events(20)
        high_threat_events = db_manager.get_high_threat_events(0.7, 50)
        
        dashboard_data = {
            'total_events': len(recent_events),
            'high_threats': len(high_threat_events),
            'recent_events': recent_events[:10],  # Show only 10 most recent
            'status': 'active'
        }
        
        return jsonify(dashboard_data)
        
    except Exception as e:
        logger.error(f"❌ Error in dashboard API: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/events')
def api_events():
    '''API endpoint for all events'''
    try:
        limit = request.args.get('limit', 100, type=int)
        events = db_manager.get_recent_events(limit)
        return jsonify(events)
    except Exception as e:
        logger.error(f"❌ Error in events API: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts', methods=['POST'])
def api_alerts():
    '''Webhook endpoint for receiving alerts'''
    try:
        alert_data = request.get_json()
        logger.info(f"🚨 Received alert: {alert_data}")
        
        # Here you could process the alert further
        # For now, just log it
        
        return jsonify({'status': 'received'}), 200
    except Exception as e:
        logger.error(f"❌ Error processing alert: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("🌐 Starting EDR Web Dashboard...")
    app.run(host='0.0.0.0', port=5000, debug=False)