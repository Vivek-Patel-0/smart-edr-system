'''
File Monitor - Watches files and folders for suspicious activity
Like having a security camera for your files!
'''

import os
import time
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from utils.logger import setup_logger

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        self.logger = setup_logger('FileMonitor')
        
    def on_any_event(self, event):
        '''Handle any file system event'''
        if event.is_directory:
            return
            
        event_data = {
            'type': 'file_event',
            'action': event.event_type,
            'path': event.src_path,
            'timestamp': time.time(),
            'is_directory': event.is_directory
        }
        
        # Log the event
        self.logger.info(f"📁 File {event.event_type}: {event.src_path}")
        
        # Send to main agent
        self.callback(event_data)

class FileMonitor:
    def __init__(self, watch_paths: list):
        self.watch_paths = watch_paths
        self.logger = setup_logger('FileMonitor')
        self.observer = Observer()
        self.callback = None
        self.running = False
        
    def set_callback(self, callback):
        '''Set callback function for events'''
        self.callback = callback
        
    def start(self):
        '''Start monitoring files'''
        if not self.callback:
            raise ValueError("Callback function not set!")
            
        self.running = True
        event_handler = FileEventHandler(self.callback)
        
        # Watch each path
        for path in self.watch_paths:
            if os.path.exists(path):
                self.observer.schedule(event_handler, path, recursive=True)
                self.logger.info(f"👁️  Watching: {path}")
            else:
                self.logger.warning(f"⚠️  Path not found: {path}")
        
        self.observer.start()
        self.logger.info("✅ File monitoring started")
        
    def stop(self):
        '''Stop monitoring files'''
        self.running = False
        self.observer.stop()
        self.observer.join()
        self.logger.info("🔴 File monitoring stopped")