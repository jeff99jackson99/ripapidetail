"""
Configuration management utilities
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def load_config() -> Dict[str, Any]:
    """Load configuration from various sources"""
    config = {}
    
    # Default configuration
    default_config = {
        "max_depth": 3,
        "timeout": 30,
        "github_token": None,
        "selenium_enabled": False,
        "chrome_driver_path": None,
        "log_level": "INFO"
    }
    
    # Load from environment variables
    env_config = {
        "github_token": os.getenv("GITHUB_TOKEN"),
        "max_depth": int(os.getenv("MAX_DEPTH", default_config["max_depth"])),
        "timeout": int(os.getenv("TIMEOUT", default_config["timeout"])),
        "selenium_enabled": os.getenv("SELENIUM_ENABLED", "false").lower() == "true",
        "chrome_driver_path": os.getenv("CHROME_DRIVER_PATH"),
        "log_level": os.getenv("LOG_LEVEL", default_config["log_level"])
    }
    
    # Load from config files
    config_files = [
        "config.json",
        "config.yaml",
        "config.yml",
        ".env"
    ]
    
    for config_file in config_files:
        config_path = Path(config_file)
        if config_path.exists():
            try:
                if config_file.endswith('.json'):
                    with open(config_path, 'r') as f:
                        file_config = json.load(f)
                elif config_file.endswith(('.yaml', '.yml')):
                    with open(config_path, 'r') as f:
                        file_config = yaml.safe_load(f)
                elif config_file == '.env':
                    file_config = load_env_file(config_path)
                else:
                    continue
                
                config.update(file_config)
                logger.info(f"Loaded configuration from {config_file}")
                
            except Exception as e:
                logger.warning(f"Failed to load config file {config_file}: {str(e)}")
    
    # Merge configurations (env vars take precedence)
    final_config = default_config.copy()
    final_config.update(config)
    final_config.update(env_config)
    
    return final_config

def load_env_file(env_path: Path) -> Dict[str, Any]:
    """Load environment variables from .env file"""
    env_config = {}
    
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_config[key.strip()] = value.strip()
    except Exception as e:
        logger.warning(f"Failed to load .env file: {str(e)}")
    
    return env_config

def save_config(config: Dict[str, Any], filename: str = "config.json"):
    """Save configuration to file"""
    try:
        config_path = Path(filename)
        
        if filename.endswith('.json'):
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
        elif filename.endswith(('.yaml', '.yml')):
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
        
        logger.info(f"Configuration saved to {filename}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save configuration: {str(e)}")
        return False
