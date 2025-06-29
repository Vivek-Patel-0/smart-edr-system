#!/usr/bin/env python3
'''
Smart EDR System - Main Entry Point
Like the main control center of our security system!
'''

import sys
import time
import signal
import threading
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from core.agent import EDRAgent
from utils.logger import setup_logger
from utils.config import load_config

class SmartEDRSystem:
    def __init__(self):
        self.logger = setup_logger('SmartEDR')
        self.config = load_config()
        self.agent = None
        self.running = False
        
    def start(self):
        '''Start the EDR system'''
        self.logger.info("🚀 Starting Smart EDR System...")
        
        try:
            # Initialize EDR Agent
            self.agent = EDRAgent(self.config)
            
            # Start monitoring
            self.agent.start_monitoring()
            
            self.running = True
            self.logger.info("✅ Smart EDR System is running!")
            
            # Keep the system running
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.logger.info("👋 Shutting down gracefully...")
            self.stop()
        except Exception as e:
            self.logger.error(f"❌ Error starting EDR system: {e}")
            
    def stop(self):
        '''Stop the EDR system'''
        self.running = False
        if self.agent:
            self.agent.stop_monitoring()
        self.logger.info("🛑 Smart EDR System stopped")

def signal_handler(signum, frame):
    '''Handle system signals'''
    print("\\n⚠️  Received shutdown signal...")
    sys.exit(0)

if __name__ == "__main__":
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start the EDR system
    edr_system = SmartEDRSystem()
    edr_system.start()