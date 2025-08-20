"""
Enhanced URL handling with automatic password protection detection
"""

import requests
import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import json

logger = logging.getLogger(__name__)

class EnhancedURLHandler:
    """Enhanced URL handler with password protection detection"""
    
    def __init__(self, session: Optional[requests.Session] = None):
        self.session = session or requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Common password protection indicators
        self.password_indicators = [
            'password',
            'login',
            'signin',
            'authenticate',
            'auth',
            'secure',
            'protected',
            'restricted',
            'members-only',
            'private'
        ]
        
        # Common authentication form patterns
        self.auth_patterns = [
            r'<form[^>]*action[^>]*login[^>]*>',
            r'<form[^>]*action[^>]*signin[^>]*>',
            r'<form[^>]*action[^>]*auth[^>]*>',
            r'<input[^>]*name[^>]*password[^>]*>',
            r'<input[^>]*type[^>]*password[^>]*>',
            r'<input[^>]*name[^>]*username[^>]*>',
            r'<input[^>]*name[^>]*email[^>]*>'
        ]
    
    def analyze_url(self, url: str) -> Dict[str, Any]:
        """Analyze a URL for password protection and authentication requirements"""
        try:
            logger.info(f"Analyzing URL: {url}")
            
            # Basic URL validation
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = 'https://' + url
                parsed_url = urlparse(url)
            
            # Check if URL is accessible
            try:
                response = self.session.get(url, timeout=10, allow_redirects=True)
                final_url = response.url
                status_code = response.status_code
            except requests.exceptions.RequestException as e:
                return {
                    "url": url,
                    "accessible": False,
                    "error": str(e),
                    "password_protected": False,
                    "auth_required": False,
                    "recommendations": ["Check if the URL is correct and accessible"]
                }
            
            # Analyze the response
            analysis = {
                "url": url,
                "final_url": final_url,
                "accessible": True,
                "status_code": status_code,
                "redirected": final_url != url,
                "password_protected": False,
                "auth_required": False,
                "auth_methods": [],
                "form_fields": [],
                "recommendations": []
            }
            
            # Check for password protection indicators
            if response.status_code == 401:
                analysis["password_protected"] = True
                analysis["auth_required"] = True
                analysis["recommendations"].append("Site requires authentication (HTTP 401)")
            
            elif response.status_code == 403:
                analysis["password_protected"] = True
                analysis["auth_required"] = True
                analysis["recommendations"].append("Access forbidden - authentication required (HTTP 403)")
            
            elif response.status_code == 200:
                # Analyze content for authentication forms
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Check for authentication forms
                auth_forms = self._detect_auth_forms(soup)
                if auth_forms:
                    analysis["auth_required"] = True
                    analysis["auth_methods"] = auth_forms
                    analysis["recommendations"].append("Authentication forms detected on the page")
                
                # Check for password protection indicators in content
                content_indicators = self._check_content_indicators(soup, response.text)
                if content_indicators:
                    analysis["password_protected"] = True
                    analysis["auth_required"] = True
                    analysis["recommendations"].extend(content_indicators)
                
                # Check for API endpoints that might require authentication
                api_endpoints = self._detect_api_endpoints(soup, response.text)
                if api_endpoints:
                    analysis["api_endpoints"] = api_endpoints
                    analysis["recommendations"].append("API endpoints detected - may require authentication")
            
            # Add general recommendations
            if analysis["auth_required"]:
                analysis["recommendations"].extend([
                    "Use the 'Gated API' extraction method for this site",
                    "Prepare your login credentials before extraction",
                    "Consider using browser automation for complex authentication flows"
                ])
            else:
                analysis["recommendations"].append("Site appears to be publicly accessible")
            
            return analysis
            
        except Exception as e:
            logger.error(f"URL analysis failed: {str(e)}")
            return {
                "url": url,
                "accessible": False,
                "error": str(e),
                "password_protected": False,
                "auth_required": False,
                "recommendations": ["Analysis failed - check the URL manually"]
            }
    
    def _detect_auth_forms(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Detect authentication forms on the page"""
        auth_forms = []
        
        # Find all forms
        forms = soup.find_all('form')
        
        for form in forms:
            form_info = {
                "action": form.get('action', ''),
                "method": form.get('method', 'GET'),
                "fields": [],
                "auth_likelihood": 0
            }
            
            # Check form inputs
            inputs = form.find_all(['input', 'select', 'textarea'])
            auth_fields = 0
            
            for input_elem in inputs:
                input_type = input_elem.get('type', 'text')
                input_name = input_elem.get('name', '')
                input_id = input_elem.get('id', '')
                
                field_info = {
                    "type": input_type,
                    "name": input_name,
                    "id": input_id,
                    "required": input_elem.get('required') is not None,
                    "placeholder": input_elem.get('placeholder', '')
                }
                
                form_info["fields"].append(field_info)
                
                # Check if this looks like an authentication field
                if self._is_auth_field(input_type, input_name, input_id):
                    auth_fields += 1
            
            # Calculate authentication likelihood
            if auth_fields >= 2:  # Username + password
                form_info["auth_likelihood"] = 0.9
            elif auth_fields == 1:
                form_info["auth_likelihood"] = 0.6
            else:
                form_info["auth_likelihood"] = 0.2
            
            # Only include forms with reasonable auth likelihood
            if form_info["auth_likelihood"] > 0.3:
                auth_forms.append(form_info)
        
        return auth_forms
    
    def _is_auth_field(self, input_type: str, input_name: str, input_id: str) -> bool:
        """Check if an input field is likely an authentication field"""
        field_text = f"{input_type} {input_name} {input_id}".lower()
        
        # Check for password fields
        if input_type == 'password':
            return True
        
        # Check for username/email fields
        username_indicators = ['username', 'user', 'email', 'login', 'account', 'id']
        if any(indicator in field_text for indicator in username_indicators):
            return True
        
        # Check for submit buttons
        submit_indicators = ['submit', 'login', 'signin', 'auth', 'enter']
        if any(indicator in field_text for indicator in submit_indicators):
            return True
        
        return False
    
    def _check_content_indicators(self, soup: BeautifulSoup, text: str) -> List[str]:
        """Check content for password protection indicators"""
        indicators = []
        text_lower = text.lower()
        
        # Check for password protection keywords
        for indicator in self.password_indicators:
            if indicator in text_lower:
                indicators.append(f"Password protection indicator found: '{indicator}'")
        
        # Check for authentication-related text
        auth_texts = [
            'please log in',
            'sign in required',
            'authentication required',
            'login to access',
            'members only',
            'private area',
            'restricted access'
        ]
        
        for auth_text in auth_texts:
            if auth_text in text_lower:
                indicators.append(f"Authentication text found: '{auth_text}'")
        
        # Check for login/signin links
        auth_links = soup.find_all('a', href=True)
        for link in auth_links:
            href = link.get('href', '').lower()
            link_text = link.get_text().lower()
            
            if any(indicator in href or indicator in link_text for indicator in ['login', 'signin', 'auth']):
                indicators.append(f"Authentication link found: {link.get_text().strip()}")
        
        return indicators
    
    def _detect_api_endpoints(self, soup: BeautifulSoup, text: str) -> List[Dict[str, Any]]:
        """Detect potential API endpoints on the page"""
        api_endpoints = []
        
        # Common API patterns
        api_patterns = [
            r'/api/[^\s"\'<>]+',
            r'/rest/[^\s"\'<>]+',
            r'/v\d+/[^\s"\'<>]+',
            r'/graphql[^\s"\'<>]*',
            r'/swagger[^\s"\'<>]*',
            r'/openapi[^\s"\'<>]*'
        ]
        
        # Find API endpoints in text
        for pattern in api_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                api_endpoints.append({
                    "url": match,
                    "type": "URL pattern",
                    "confidence": 0.8
                })
        
        # Find API endpoints in links
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href', '')
            if any(pattern in href.lower() for pattern in ['/api/', '/rest/', '/v1/', '/v2/', 'graphql', 'swagger']):
                api_endpoints.append({
                    "url": href,
                    "type": "Link",
                    "text": link.get_text().strip(),
                    "confidence": 0.9
                })
        
        # Find API endpoints in JavaScript
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                script_text = script.string
                for pattern in api_patterns:
                    matches = re.findall(pattern, script_text, re.IGNORECASE)
                    for match in matches:
                        api_endpoints.append({
                            "url": match,
                            "type": "JavaScript",
                            "confidence": 0.7
                        })
        
        return api_endpoints
    
    def get_extraction_recommendation(self, analysis: Dict[str, Any]) -> str:
        """Get extraction method recommendation based on URL analysis"""
        if analysis.get("auth_required"):
            return "gated_api"
        elif analysis.get("redirected"):
            return "url"  # Handle redirects
        else:
            return "url"  # Standard URL extraction
    
    def create_auth_config_suggestion(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create authentication configuration suggestions based on analysis"""
        if not analysis.get("auth_required"):
            return {}
        
        suggestion = {
            "login_url": analysis.get("final_url", analysis.get("url")),
            "username_field": "",
            "password_field": "",
            "submit_button": "",
            "success_indicator": "",
            "notes": []
        }
        
        # Analyze auth forms to suggest field names
        auth_forms = analysis.get("auth_methods", [])
        if auth_forms:
            # Use the form with highest auth likelihood
            best_form = max(auth_forms, key=lambda x: x.get("auth_likelihood", 0))
            
            for field in best_form.get("fields", []):
                field_name = field.get("name", "")
                field_type = field.get("type", "")
                
                if field_type == "password":
                    suggestion["password_field"] = field_name
                elif field_type in ["text", "email"] and not suggestion["username_field"]:
                    suggestion["username_field"] = field_name
                elif field_type == "submit":
                    suggestion["submit_button"] = f"input[name='{field_name}']"
            
            # If no submit button found, suggest a generic one
            if not suggestion["submit_button"]:
                suggestion["submit_button"] = "input[type='submit'], button[type='submit']"
        
        # Add notes based on analysis
        if analysis.get("status_code") == 401:
            suggestion["notes"].append("HTTP 401 response indicates authentication required")
        elif analysis.get("status_code") == 403:
            suggestion["notes"].append("HTTP 403 response indicates access forbidden")
        
        if analysis.get("redirected"):
            suggestion["notes"].append("URL was redirected - use final URL for authentication")
        
        return suggestion
