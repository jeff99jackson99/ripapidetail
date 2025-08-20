"""
Core extraction logic for API details from various sources
"""

import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse
import re
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class APIEndpoint:
    """Represents an API endpoint found during extraction"""
    url: str
    method: str
    parameters: Dict[str, Any]
    headers: Dict[str, str]
    description: Optional[str] = None
    confidence: float = 0.0

@dataclass
class FormData:
    """Represents a form found during extraction"""
    action: str
    method: str
    inputs: List[Dict[str, Any]]
    description: Optional[str] = None

class MenuExtractor:
    """Extracts API details from dealer menus and other sources"""
    
    def __init__(self, max_depth: int = 3, timeout: int = 30):
        self.max_depth = max_depth
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extract_from_url(self, url: str) -> Dict[str, Any]:
        """Extract API details from a URL"""
        logger.info(f"Extracting API details from URL: {url}")
        
        try:
            # Get the page content
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse the content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract various API-related information
            results = {
                "source_url": url,
                "endpoints": self._extract_endpoints(soup, url),
                "forms": self._extract_forms(soup, url),
                "javascript": self._extract_javascript(soup),
                "network_requests": self._extract_network_requests(soup),
                "api_keys": self._extract_api_keys(soup),
                "metadata": self._extract_metadata(soup, response)
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to extract from URL {url}: {str(e)}")
            raise
    
    def extract_from_content(self, content: str, source_name: str) -> Dict[str, Any]:
        """Extract API details from content string"""
        logger.info(f"Extracting API details from content: {source_name}")
        
        try:
            soup = BeautifulSoup(content, 'html.parser')
            
            results = {
                "source_name": source_name,
                "endpoints": self._extract_endpoints(soup, ""),
                "forms": self._extract_forms(soup, ""),
                "javascript": self._extract_javascript(soup),
                "network_requests": self._extract_network_requests(soup),
                "api_keys": self._extract_api_keys(soup),
                "metadata": self._extract_metadata(soup, None)
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to extract from content {source_name}: {str(e)}")
            raise
    
    def _extract_endpoints(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """Extract potential API endpoints from the page"""
        endpoints = []
        
        # Look for common API endpoint patterns
        api_patterns = [
            r'/api/',
            r'/rest/',
            r'/v\d+/',
            r'/graphql',
            r'/swagger',
            r'/openapi'
        ]
        
        # Find all links
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Check if it matches API patterns
            for pattern in api_patterns:
                if re.search(pattern, href, re.IGNORECASE):
                    full_url = urljoin(base_url, href) if base_url else href
                    
                    endpoint = {
                        "url": full_url,
                        "method": "GET",  # Default assumption
                        "parameters": {},
                        "headers": {},
                        "description": link.get_text(strip=True),
                        "confidence": 0.8
                    }
                    
                    endpoints.append(endpoint)
        
        # Look for JavaScript fetch/axios calls
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                # Find fetch calls
                fetch_matches = re.findall(r'fetch\(["\']([^"\']+)["\']', script.string)
                for match in fetch_matches:
                    full_url = urljoin(base_url, match) if base_url else match
                    
                    endpoint = {
                        "url": full_url,
                        "method": "GET",
                        "parameters": {},
                        "headers": {},
                        "description": "Found in JavaScript fetch call",
                        "confidence": 0.9
                    }
                    
                    endpoints.append(endpoint)
        
        return endpoints
    
    def _extract_forms(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """Extract form information"""
        forms = []
        
        for form in soup.find_all('form'):
            form_data = {
                "action": urljoin(base_url, form.get('action', '')) if base_url else form.get('action', ''),
                "method": form.get('method', 'GET').upper(),
                "inputs": [],
                "description": "Form found in page"
            }
            
            # Extract form inputs
            for input_tag in form.find_all(['input', 'select', 'textarea']):
                input_data = {
                    "name": input_tag.get('name', ''),
                    "type": input_tag.get('type', 'text'),
                    "required": input_tag.get('required') is not None,
                    "placeholder": input_tag.get('placeholder', ''),
                    "value": input_tag.get('value', '')
                }
                
                form_data["inputs"].append(input_data)
            
            forms.append(form_data)
        
        return forms
    
    def _extract_javascript(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract JavaScript API calls"""
        javascript_data = []
        
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                # Look for various API call patterns
                patterns = [
                    (r'fetch\(["\']([^"\']+)["\']', 'fetch'),
                    (r'axios\.(get|post|put|delete)\(["\']([^"\']+)["\']', 'axios'),
                    (r'\.ajax\([^)]*url:\s*["\']([^"\']+)["\']', 'jquery_ajax'),
                    (r'XMLHttpRequest[^}]*open\(["\']([^"\']+)["\']', 'xmlhttprequest')
                ]
                
                for pattern, call_type in patterns:
                    matches = re.findall(pattern, script.string, re.IGNORECASE)
                    for match in matches:
                        if isinstance(match, tuple):
                            url = match[1] if len(match) > 1 else match[0]
                        else:
                            url = match
                        
                        js_data = {
                            "type": call_type,
                            "code": script.string,
                            "url": url,
                            "description": f"{call_type} API call found"
                        }
                        
                        javascript_data.append(js_data)
        
        return javascript_data
    
    def _extract_network_requests(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract potential network request patterns"""
        network_requests = []
        
        # Look for common API request patterns in HTML attributes
        elements = soup.find_all(attrs={"data-api": True})
        for element in elements:
            request_data = {
                "url": element.get('data-api', ''),
                "method": element.get('data-method', 'GET'),
                "parameters": {},
                "description": f"Data API attribute found on {element.name}"
            }
            
            network_requests.append(request_data)
        
        return network_requests
    
    def _extract_api_keys(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract potential API keys or tokens"""
        api_keys = []
        
        # Look for common API key patterns
        key_patterns = [
            r'api[_-]?key["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'bearer["\']?\s*[:=]\s*["\']([^"\']+)["\']'
        ]
        
        # Search in script tags and other text content
        for script in soup.find_all('script'):
            if script.string:
                for pattern in key_patterns:
                    matches = re.findall(pattern, script.string, re.IGNORECASE)
                    for match in matches:
                        api_keys.append({
                            "type": "API Key",
                            "value": match[:10] + "..." if len(match) > 10 else match,
                            "description": "API key found in JavaScript"
                        })
        
        return api_keys
    
    def _extract_metadata(self, soup: BeautifulSoup, response) -> Dict[str, Any]:
        """Extract metadata about the page"""
        metadata = {}
        
        # Extract meta tags
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                metadata[name] = content
        
        # Extract title
        title = soup.find('title')
        if title:
            metadata['title'] = title.get_text(strip=True)
        
        # Extract response headers if available
        if response:
            metadata['response_headers'] = dict(response.headers)
            metadata['status_code'] = response.status_code
        
        return metadata
    
    async def extract_with_selenium(self, url: str) -> Dict[str, Any]:
        """Extract API details using Selenium for dynamic content"""
        logger.info(f"Extracting with Selenium from URL: {url}")
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = None
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Get the page source after JavaScript execution
            page_source = driver.page_source
            
            # Extract network requests from browser dev tools (if possible)
            # This is a simplified approach - in production you might want to use
            # browser dev tools protocol for more detailed network analysis
            
            return self.extract_from_content(page_source, url)
            
        except Exception as e:
            logger.error(f"Selenium extraction failed: {str(e)}")
            raise
        finally:
            if driver:
                driver.quit()
    
    def close(self):
        """Clean up resources"""
        if hasattr(self, 'session'):
            self.session.close()
