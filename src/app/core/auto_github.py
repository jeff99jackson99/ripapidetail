"""
Automatic GitHub token management and detection
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import subprocess
import re

logger = logging.getLogger(__name__)

class AutoGitHubManager:
    """Automatically manages GitHub tokens from various sources"""
    
    def __init__(self):
        self.token = None
        self.token_source = None
        self.token_info = {}
    
    def auto_detect_token(self) -> Optional[str]:
        """Automatically detect GitHub token from various sources"""
        # Priority order for token detection
        detection_methods = [
            self._get_from_env,
            self._get_from_git_config,
            self._get_from_gh_cli,
            self._get_from_keychain,
            self._get_from_common_locations
        ]
        
        for method in detection_methods:
            try:
                token = method()
                if token and self._validate_token(token):
                    logger.info(f"GitHub token detected from: {method.__name__}")
                    return token
            except Exception as e:
                logger.debug(f"Token detection method {method.__name__} failed: {str(e)}")
        
        logger.warning("No valid GitHub token found automatically")
        return None
    
    def _get_from_env(self) -> Optional[str]:
        """Get token from environment variables"""
        env_vars = [
            'GITHUB_TOKEN',
            'GITHUB_ACCESS_TOKEN',
            'GH_TOKEN',
            'GITHUB_PERSONAL_ACCESS_TOKEN'
        ]
        
        for var in env_vars:
            token = os.getenv(var)
            if token:
                self.token_source = f"Environment variable: {var}"
                return token
        
        return None
    
    def _get_from_git_config(self) -> Optional[str]:
        """Get token from git configuration"""
        try:
            # Check global git config
            result = subprocess.run(
                ['git', 'config', '--global', '--get', 'github.token'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                self.token_source = "Git global config"
                return result.stdout.strip()
            
            # Check local git config
            result = subprocess.run(
                ['git', 'config', '--local', '--get', 'github.token'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                self.token_source = "Git local config"
                return result.stdout.strip()
                
        except Exception as e:
            logger.debug(f"Git config check failed: {str(e)}")
        
        return None
    
    def _get_from_gh_cli(self) -> Optional[str]:
        """Get token from GitHub CLI if installed"""
        try:
            result = subprocess.run(
                ['gh', 'auth', 'token'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                self.token_source = "GitHub CLI"
                return result.stdout.strip()
                
        except Exception as e:
            logger.debug(f"GitHub CLI check failed: {str(e)}")
        
        return None
    
    def _get_from_keychain(self) -> Optional[str]:
        """Get token from system keychain (macOS)"""
        try:
            if os.name == 'posix' and os.uname().sysname == 'Darwin':
                result = subprocess.run([
                    'security', 'find-generic-password',
                    '-s', 'github.com',
                    '-a', os.getenv('USER', ''),
                    '-w'
                ], capture_output=True, text=True, timeout=5)
                
                if result.returncode == 0 and result.stdout.strip():
                    self.token_source = "macOS Keychain"
                    return result.stdout.strip()
                    
        except Exception as e:
            logger.debug(f"Keychain check failed: {str(e)}")
        
        return None
    
    def _get_from_common_locations(self) -> Optional[str]:
        """Get token from common configuration file locations"""
        common_paths = [
            Path.home() / '.github' / 'token',
            Path.home() / '.config' / 'gh' / 'hosts.yml',
            Path.home() / '.git-credentials',
            Path.home() / '.netrc'
        ]
        
        for path in common_paths:
            try:
                if path.exists():
                    token = self._extract_token_from_file(path)
                    if token:
                        self.token_source = f"File: {path}"
                        return token
            except Exception as e:
                logger.debug(f"File check failed for {path}: {str(e)}")
        
        return None
    
    def _extract_token_from_file(self, file_path: Path) -> Optional[str]:
        """Extract token from various file formats"""
        try:
            content = file_path.read_text()
            
            # Check for plain token
            if re.match(r'^[a-zA-Z0-9]{35,}$', content.strip()):
                return content.strip()
            
            # Check for JSON format
            if file_path.suffix == '.yml' or file_path.suffix == '.yaml':
                import yaml
                data = yaml.safe_load(content)
                if isinstance(data, dict):
                    token = self._find_token_in_dict(data)
                    if token:
                        return token
            
            # Check for git credentials format
            if 'github.com' in content:
                lines = content.split('\n')
                for line in lines:
                    if 'github.com' in line:
                        parts = line.split(':')
                        if len(parts) >= 3:
                            token = parts[2].split('@')[0]
                            if self._validate_token(token):
                                return token
            
            # Check for netrc format
            if 'github.com' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'github.com' in line and i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not next_line.startswith('#'):
                            token = next_line
                            if self._validate_token(token):
                                return token
                                
        except Exception as e:
            logger.debug(f"Token extraction failed from {file_path}: {str(e)}")
        
        return None
    
    def _find_token_in_dict(self, data: Dict[str, Any], max_depth: int = 5) -> Optional[str]:
        """Recursively search for token in dictionary"""
        if max_depth <= 0:
            return None
        
        for key, value in data.items():
            if isinstance(value, str) and self._validate_token(value):
                return value
            elif isinstance(value, dict):
                token = self._find_token_in_dict(value, max_depth - 1)
                if token:
                    return token
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        token = self._find_token_in_dict(item, max_depth - 1)
                        if token:
                            return token
        
        return None
    
    def _validate_token(self, token: str) -> bool:
        """Validate GitHub token format"""
        if not token or len(token) < 35:
            return False
        
        # GitHub tokens are typically 40 characters (classic) or 35+ (fine-grained)
        if not re.match(r'^[a-zA-Z0-9_]{35,}$', token):
            return False
        
        return True
    
    def get_token_info(self) -> Dict[str, Any]:
        """Get information about the current token"""
        if not self.token:
            return {}
        
        return {
            "token": self.token[:8] + "..." + self.token[-4:],  # Masked
            "source": self.token_source,
            "length": len(self.token),
            "is_valid": self._validate_token(self.token)
        }
    
    def set_token(self, token: str, source: str = "Manual"):
        """Set a token manually"""
        if self._validate_token(token):
            self.token = token
            self.token_source = source
            logger.info(f"GitHub token set from: {source}")
        else:
            raise ValueError("Invalid GitHub token format")
    
    def clear_token(self):
        """Clear the current token"""
        self.token = None
        self.token_source = None
        logger.info("GitHub token cleared")
    
    def is_available(self) -> bool:
        """Check if a valid token is available"""
        return self.token is not None and self._validate_token(self.token)
