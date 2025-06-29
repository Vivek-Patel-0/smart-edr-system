'''
Configuration Loader - Reads settings from config file
Like reading instructions before building something!
'''

import yaml
import os
from pathlib import Path
from utils.logger import setup_logger

def load_config(config_path='config.yaml'):
    '''Load configuration from YAML file'''
    logger = setup_logger('Config')
    
    try:
        config_file = Path(config_path)
        
        if not config_file.exists():
            logger.warning(f"⚠️  Config file not found: {config_path}, using defaults")
            return get_default_config()
        
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"✅ Configuration loaded from {config_path}")
        return config
        
    except Exception as e:
        logger.error(f"❌ Error loading config: {e}")
        return get_default_config()

def get_default_config():
    '''Get default configuration'''
    return {
        'edr': {
            'agent_name': 'SmartEDR-Agent',
            'log_level': 'INFO'
        },
        'monitoring': {
            'file_paths': [
                os.path.expanduser('~/Documents'),
                os.path.expanduser('~/Downloads')
            ],
            'process_monitoring': True,
            'network_monitoring': True
        },
        'database': {
            'type': 'sqlite',
            'path': 'data/edr.db'
        },
        'alerts': {
            'email_enabled': False,
            'webhook_enabled': True,
            'webhook_url': 'http://localhost:5000/alerts'
        },
        'ai': {
            'enable_ml': True,
            'model_path': 'data/models/',
            'training_data_path': 'data/training/'
        }
    }