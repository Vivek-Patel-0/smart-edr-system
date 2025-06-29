'''
Alert Manager - Sends notifications when threats are detected
Like a security alarm that tells everyone when something's wrong!
'''

import json
import requests
import time
from utils.logger import setup_logger

class AlertManager:
    def __init__(self, config):
        self.config = config
        self.logger = setup_logger('AlertManager')
        
    def send_alert(self, event_data, threat_score):
        '''Send alert based on configuration'''
        alert_message = self._create_alert_message(event_data, threat_score)
        
        # Log the alert
        self.logger.warning(f"🚨 ALERT: {alert_message}")
        
        # Send webhook alert
        if self.config.get('webhook_enabled', False):
            self._send_webhook_alert(alert_message, event_data, threat_score)
        
        # Send email alert (placeholder)
        if self.config.get('email_enabled', False):
            self._send_email_alert(alert_message, event_data, threat_score)
    
    def _create_alert_message(self, event_data, threat_score):
        '''Create a human-readable alert message'''
        event_type = event_data.get('type', 'unknown')
        action = event_data.get('action', 'unknown')
        
        if event_type == 'file_event':
            path = event_data.get('path', 'unknown')
            return f"Suspicious file activity: {action} on {path} (Threat Score: {threat_score:.2f})"
        
        elif event_type == 'process_event':
            name = event_data.get('name', 'unknown')
            pid = event_data.get('pid', 'unknown')
            return f"Suspicious process activity: {name} (PID: {pid}) - {action} (Threat Score: {threat_score:.2f})"
        
        elif event_type == 'network_event':
            remote_addr = event_data.get('remote_addr', 'unknown')
            return f"Suspicious network activity: Connection to {remote_addr} (Threat Score: {threat_score:.2f})"
        
        return f"Unknown suspicious activity detected (Threat Score: {threat_score:.2f})"
    
    def _send_webhook_alert(self, message, event_data, threat_score):
        '''Send alert via webhook'''
        try:
            webhook_url = self.config.get('webhook_url')
            if not webhook_url:
                return
            
            payload = {
                'alert_type': 'threat_detected',
                'message': message,
                'threat_score': threat_score,
                'event_data': event_data,
                'timestamp': time.time()
            }
            
            response = requests.post(
                webhook_url,
                json=payload,
                timeout=5
            )
            
            if response.status_code == 200:
                self.logger.info("✅ Webhook alert sent successfully")
            else:
                self.logger.error(f"❌ Webhook alert failed: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"❌ Error sending webhook alert: {e}")
    
    def _send_email_alert(self, message, event_data, threat_score):
        '''Send alert via email (placeholder)'''
        # This would integrate with an email service
        self.logger.info(f"📧 Email alert would be sent: {message}")