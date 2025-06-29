'''
Anomaly Detector - The AI brain that detects suspicious behavior
Like a smart detective that learns what's normal and what's not!
'''

import numpy as np
import pickle
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from utils.logger import setup_logger

class AnomalyDetector:
    def __init__(self):
        self.logger = setup_logger('AnomalyDetector')
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def extract_features(self, event_data):
        '''Extract features from event data for AI analysis'''
        features = []
        
        # Basic features
        features.append(event_data.get('timestamp', 0))
        
        # Event type encoding
        event_types = {'file_event': 1, 'process_event': 2, 'network_event': 3}
        features.append(event_types.get(event_data.get('type', ''), 0))
        
        # Action encoding
        actions = {'created': 1, 'modified': 2, 'deleted': 3, 'moved': 4, 'new_connection': 5}
        features.append(actions.get(event_data.get('action', ''), 0))
        
        # Path/Name features (simplified)
        if 'path' in event_data:
            path = event_data['path']
            features.append(len(path))  # Path length
            features.append(1 if '.exe' in path.lower() else 0)  # Is executable
            features.append(1 if 'system32' in path.lower() else 0)  # Is system file
        else:
            features.extend([0, 0, 0])
            
        # Process features
        if 'pid' in event_data:
            features.append(event_data['pid'])
        else:
            features.append(0)
            
        # Pad or truncate to fixed size
        while len(features) < 10:
            features.append(0)
        
        return np.array(features[:10])
    
    def analyze_event(self, event_data):
        '''Analyze an event and return threat score'''
        try:
            features = self.extract_features(event_data)
            
            if not self.is_trained:
                # Simple rule-based scoring for untrained model
                return self._rule_based_scoring(event_data)
            
            # Use ML model
            features_scaled = self.scaler.transform([features])
            anomaly_score = self.model.decision_function(features_scaled)[0]
            
            # Convert to 0-1 scale (higher = more suspicious)
            threat_score = max(0, min(1, (0.5 - anomaly_score) * 2))
            
            return threat_score
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing event: {e}")
            return 0.5  # Default medium threat score
    
    def _rule_based_scoring(self, event_data):
        '''Simple rule-based threat scoring'''
        score = 0.0
        
        # Suspicious file operations
        if event_data.get('type') == 'file_event':
            path = event_data.get('path', '').lower()
            if any(suspicious in path for suspicious in ['.exe', '.bat', '.cmd', '.scr']):
                score += 0.3
            if 'system32' in path:
                score += 0.4
            if event_data.get('action') == 'deleted':
                score += 0.2
                
        # Suspicious process operations
        elif event_data.get('type') == 'process_event':
            name = event_data.get('name', '').lower()
            if any(suspicious in name for suspicious in ['cmd', 'powershell', 'wscript']):
                score += 0.5
                
        # Network connections
        elif event_data.get('type') == 'network_event':
            score += 0.2  # Any new connection is slightly suspicious
        
        return min(1.0, score)
    
    def train_model(self, training_data):
        '''Train the anomaly detection model'''
        self.logger.info("🧠 Training anomaly detection model...")
        
        try:
            features_list = []
            for event in training_data:
                features = self.extract_features(event)
                features_list.append(features)
            
            if len(features_list) < 10:
                self.logger.warning("⚠️  Not enough training data, using rule-based detection")
                return
            
            X = np.array(features_list)
            X_scaled = self.scaler.fit_transform(X)
            
            self.model.fit(X_scaled)
            self.is_trained = True
            
            self.logger.info("✅ Model training completed!")
            
        except Exception as e:
            self.logger.error(f"❌ Error training model: {e}")
    
    def save_model(self, filepath):
        '''Save the trained model'''
        try:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'is_trained': self.is_trained
            }
            with open(filepath, 'wb') as f:
                pickle.dump(model_data, f)
            self.logger.info(f"💾 Model saved to {filepath}")
        except Exception as e:
            self.logger.error(f"❌ Error saving model: {e}")
    
    def load_model(self, filepath):
        '''Load a trained model'''
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.is_trained = model_data['is_trained']
            
            self.logger.info(f"📂 Model loaded from {filepath}")
        except Exception as e:
            self.logger.error(f"❌ Error loading model: {e}")