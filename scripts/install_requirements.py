#!/usr/bin/env python3
'''
Requirements Installation Script
'''

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    '''Install Python requirements'''
    project_root = Path(__file__).parent.parent
    requirements_file = project_root / 'requirements.txt'
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found!")
        return False
    
    print("📦 Installing Python packages...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
        ])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_directories():
    '''Create necessary directories'''
    project_root = Path(__file__).parent.parent
    
    directories = [
        'data/logs',
        'data/models', 
        'data/training/benign_samples',
        'data/training/malicious_samples',
        'data/db'
    ]
    
    print("📁 Creating directories...")
    for dir_path in directories:
        full_path = project_root / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {dir_path}")

if __name__ == "__main__":
    print("🔧 Setting up Smart EDR System...")
    
    create_directories()
    if install_requirements():
        print("🎉 Setup completed successfully!")
        print("\\n🚀 You can now start the EDR system:")
        print("   python scripts/start_edr.py")
        print("\\n🌐 Or start the web dashboard:")
        print("   python scripts/start_dashboard.py")
    else:
        print("❌ Setup failed!")