#!/usr/bin/env python3
'''
EDR Startup Script - Easy way to start the EDR system
'''

import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / 'src'))
# Ensure the src directory is in the path
if str(project_root / 'src') not in sys.path:
    sys.path.append(str(project_root / 'src'))
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.main import SmartEDRSystem

def main():
    print("🚀 Starting Smart EDR System...")
    print("📁 Project directory:", project_root)
    
    # Create necessary directories
    (project_root / 'data' / 'logs').mkdir(parents=True, exist_ok=True)
    (project_root / 'data' / 'models').mkdir(parents=True, exist_ok=True)
    (project_root / 'data' / 'training').mkdir(parents=True, exist_ok=True)
    
    # Start EDR system
    edr_system = SmartEDRSystem()
    try:
        edr_system.start()
    except KeyboardInterrupt:
        print("\\n👋 Goodbye!")
        edr_system.stop()

if __name__ == "__main__":
    main()