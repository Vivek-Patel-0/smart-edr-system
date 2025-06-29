'''
Process Monitor - Watches running processes
Like keeping track of who's in the building!
'''

import psutil
import time
import threading
from utils.logger import setup_logger

class ProcessMonitor:
    def __init__(self):
        self.logger = setup_logger('ProcessMonitor')
        self.callback = None
        self.running = False
        self.known_processes = set()
        self.monitor_thread = None
        
    def set_callback(self, callback):
        '''Set callback function for events'''
        self.callback = callback
        
    def start(self):
        '''Start monitoring processes'''
        if not self.callback:
            raise ValueError("Callback function not set!")
            
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_processes)
        self.monitor_thread.start()
        self.logger.info("✅ Process monitoring started")
        
    def stop(self):
        '''Stop monitoring processes'''
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join()
        self.logger.info("🔴 Process monitoring stopped")
        
    def _monitor_processes(self):
        '''Monitor processes in background'''
        while self.running:
            try:
                current_processes = set()
                
                for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
                    try:
                        proc_info = proc.info
                        proc_id = proc_info['pid']
                        current_processes.add(proc_id)
                        
                        # Check for new processes
                        if proc_id not in self.known_processes:
                            event_data = {
                                'type': 'process_event',
                                'action': 'created',
                                'pid': proc_id,
                                'name': proc_info['name'],
                                'cmdline': proc_info['cmdline'],
                                'timestamp': time.time()
                            }
                            
                            self.logger.info(f"🔄 New process: {proc_info['name']} (PID: {proc_id})")
                            if self.callback is not None:
                                self.callback(event_data)
                            
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                # Update known processes
                self.known_processes = current_processes
                
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                self.logger.error(f"❌ Error monitoring processes: {e}")
                time.sleep(5)