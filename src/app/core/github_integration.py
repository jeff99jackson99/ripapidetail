"""
GitHub integration for configuration and updates
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class GitHubIntegration:
    """Handles GitHub repository integration for configuration and updates"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.current_repo = None
        
        if self.token:
            try:
                # Import PyGithub only if token is available
                from github import Github
                self.github = Github(self.token)
                logger.info("GitHub integration initialized successfully")
            except ImportError:
                logger.warning("PyGithub not installed. GitHub integration disabled.")
                self.github = None
            except Exception as e:
                logger.error(f"Failed to initialize GitHub integration: {str(e)}")
                self.github = None
        else:
            self.github = None
            logger.info("No GitHub token provided. GitHub integration disabled.")
    
    def sync_repository(self, repo_url: str, branch: str = "main") -> bool:
        """Sync with a GitHub repository"""
        try:
            if not self.github:
                raise Exception("GitHub integration not available")
            
            # Parse repository URL
            repo_name = self._parse_repo_url(repo_url)
            if not repo_name:
                raise Exception("Invalid repository URL")
            
            # Get repository
            repo = self.github.get_repo(repo_name)
            self.current_repo = repo
            
            # Get latest commit
            latest_commit = repo.get_branch(branch).commit
            
            # Download configuration files
            config_files = self._download_config_files(repo, branch)
            
            # Update local configuration
            self._update_local_config(config_files)
            
            logger.info(f"Successfully synced with repository: {repo_name}")
            return True
            
        except Exception as e:
            logger.error(f"Repository sync failed: {str(e)}")
            raise
    
    def _parse_repo_url(self, repo_url: str) -> Optional[str]:
        """Parse GitHub repository URL to owner/repo format"""
        if 'github.com' in repo_url:
            # Extract owner/repo from URL
            parts = repo_url.split('github.com/')
            if len(parts) > 1:
                repo_path = parts[1].rstrip('/')
                if repo_path.endswith('.git'):
                    repo_path = repo_path[:-4]
                return repo_path
        elif '/' in repo_url and 'github.com' not in repo_url:
            # Assume it's already in owner/repo format
            return repo_url
        
        return None
    
    def _download_config_files(self, repo, branch: str) -> Dict[str, Any]:
        """Download configuration files from repository"""
        config_files = {}
        
        # List of configuration files to look for
        config_file_names = [
            'config.json',
            'config.yaml',
            'config.yml',
            'api-ripper.json',
            'api-ripper.yaml',
            'api-ripper.yml'
        ]
        
        try:
            contents = repo.get_contents("", ref=branch)
            
            for content_file in contents:
                if content_file.name in config_file_names:
                    try:
                        file_content = content_file.decoded_content.decode('utf-8')
                        
                        if content_file.name.endswith('.json'):
                            config_files[content_file.name] = json.loads(file_content)
                        elif content_file.name.endswith(('.yaml', '.yml')):
                            config_files[content_file.name] = yaml.safe_load(file_content)
                        
                        logger.info(f"Downloaded config file: {content_file.name}")
                        
                    except Exception as e:
                        logger.warning(f"Failed to parse config file {content_file.name}: {str(e)}")
            
        except Exception as e:
            logger.error(f"Failed to download config files: {str(e)}")
        
        return config_files
    
    def _update_local_config(self, config_files: Dict[str, Any]):
        """Update local configuration with downloaded files"""
        config_dir = Path("config")
        config_dir.mkdir(exist_ok=True)
        
        for filename, content in config_files.items():
            config_path = config_dir / filename
            
            try:
                if filename.endswith('.json'):
                    with open(config_path, 'w') as f:
                        json.dump(content, f, indent=2)
                elif filename.endswith(('.yaml', '.yml')):
                    with open(config_path, 'w') as f:
                        yaml.dump(content, f, default_flow_style=False)
                
                logger.info(f"Updated local config file: {filename}")
                
            except Exception as e:
                logger.error(f"Failed to update local config {filename}: {str(e)}")
    
    def get_repository_info(self, repo_url: str) -> Optional[Dict[str, Any]]:
        """Get information about a repository"""
        try:
            if not self.github:
                return None
            
            repo_name = self._parse_repo_url(repo_url)
            if not repo_name:
                return None
            
            repo = self.github.get_repo(repo_name)
            
            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "language": repo.language,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "last_updated": repo.updated_at.isoformat(),
                "default_branch": repo.default_branch
            }
            
        except Exception as e:
            logger.error(f"Failed to get repository info: {str(e)}")
            return None
    
    def create_issue(self, repo_url: str, title: str, body: str) -> Optional[str]:
        """Create an issue in the repository"""
        try:
            if not self.github:
                return None
            
            repo_name = self._parse_repo_url(repo_url)
            if not repo_name:
                return None
            
            repo = self.github.get_repo(repo_name)
            issue = repo.create_issue(title=title, body=body)
            
            logger.info(f"Created issue: {issue.number}")
            return f"https://github.com/{repo_name}/issues/{issue.number}"
            
        except Exception as e:
            logger.error(f"Failed to create issue: {str(e)}")
            return None
    
    def get_file_content(self, repo_url: str, file_path: str, branch: str = "main") -> Optional[str]:
        """Get content of a specific file from repository"""
        try:
            if not self.github:
                return None
            
            repo_name = self._parse_repo_url(repo_url)
            if not repo_name:
                return None
            
            repo = self.github.get_repo(repo_name)
            content = repo.get_contents(file_path, ref=branch)
            
            return content.decoded_content.decode('utf-8')
            
        except Exception as e:
            logger.error(f"Failed to get file content: {str(e)}")
            return None
