'''
Network Monitor - Watches network connections
Like monitoring who's calling and who's being called!
'''

import psutil
import time
import threading
from utils.logger import setup_logger

class NetworkMonitor:
    def __init__(self):
        self.logger = setup_logger('NetworkMonitor')
        self.callback = None
        self.running = False
        self.known_connections = set()
        self.monitor_thread = None
        
    def set_callback(self, callback):
        '''Set callback function for events'''
        self.callback = callback
        
    def start(self):
        '''Start monitoring network connections'''
        if not self.callback:
            raise ValueError("Callback function not set!")
            
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_network)
        self.monitor_thread.start()
        self.logger.info("✅ Network monitoring started")
        
    def stop(self):
        '''Stop monitoring network connections'''
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join()
        self.logger.info("🔴 Network monitoring stopped")
        
    def _monitor_network(self):
        '''Monitor network connections in background'''
        while self.running:
            try:
                current_connections = set()
                
                for conn in psutil.net_connections():
                    if conn.status == 'ESTABLISHED':
                        conn_key = (conn.laddr, conn.raddr, conn.pid)
                        current_connections.add(conn_key)
                        
                        if conn_key not in self.known_connections:
                            event_data = {
                                'type': 'network_event',
                                'action': 'new_connection',
                                'local_addr': conn.laddr,
                                'remote_addr': conn.raddr,
                                'pid': conn.pid,
                                'status': conn.status,
                                'timestamp': time.time()
                            }
                            
                            self.logger.info(f"🌐 New connection: {conn.laddr} -> {conn.raddr}")
                            if self.callback:
                                self.callback(event_data)
                
                self.known_connections = current_connections
                time.sleep(3)  # Check every 3 seconds
                
            except Exception as e:
                self.logger.error(f"❌ Error monitoring network: {e}")
                time.sleep(5)