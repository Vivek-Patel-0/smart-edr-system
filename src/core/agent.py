'''
EDR Agent - The main brain of our security system
'''

import threading
import time
from typing import Dict, List

from monitors.file_monitor import FileMonitor
from monitors.process_monitor import ProcessMonitor
from monitors.network_monitor import NetworkMonitor
from ai.models.anomaly_detector import AnomalyDetector
from database.connection import DatabaseManager
from alerting.alert_manager import AlertManager
from utils.logger import setup_logger

class EDRAgent:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = setup_logger('EDRAgent')
        self.running = False
        
        # Initialize components
        self.db_manager = DatabaseManager(config['database'])
        self.alert_manager = AlertManager(config['alerts'])
        self.anomaly_detector = AnomalyDetector()
        
        # Initialize monitors
        self.monitors = {
            'file': FileMonitor(config['monitoring']['file_paths']),
            'process': ProcessMonitor(),
            'network': NetworkMonitor()
        }
        
        # Event queue for processing
        self.event_queue = []
        self.queue_lock = threading.Lock()
        
    def start_monitoring(self):
        '''Start all monitoring components'''
        self.logger.info("🔍 Starting EDR monitoring...")
        self.running = True
        
        # Start all monitors
        for name, monitor in self.monitors.items():
            monitor.set_callback(self.handle_event)
            monitor.start()
            self.logger.info(f"✅ {name.capitalize()} monitor started")
        
        # Start event processor
        self.event_processor_thread = threading.Thread(target=self.process_events)
        self.event_processor_thread.start()
        
    def stop_monitoring(self):
        '''Stop all monitoring components'''
        self.logger.info("🛑 Stopping EDR monitoring...")
        self.running = False
        
        # Stop all monitors
        for name, monitor in self.monitors.items():
            monitor.stop()
            self.logger.info(f"🔴 {name.capitalize()} monitor stopped")
            
    def handle_event(self, event_data: Dict):
        '''Handle events from monitors'''
        with self.queue_lock:
            self.event_queue.append(event_data)
            
    def process_events(self):
        '''Process events from the queue'''
        while self.running:
            if self.event_queue:
                with self.queue_lock:
                    event = self.event_queue.pop(0)
                
                # Analyze event with AI
                threat_score = self.anomaly_detector.analyze_event(event)
                
                # Store in database
                self.db_manager.store_event(event, threat_score)
                
                # Check if we need to alert
                if threat_score > 0.7:  # High threat score
                    self.alert_manager.send_alert(event, threat_score)
                    
            time.sleep(0.1)  # Small delay to prevent CPU overload