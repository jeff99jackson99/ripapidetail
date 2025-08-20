"""
Advanced extraction capabilities for gated APIs and protected content
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from pathlib import Path
import time
import base64

# Selenium imports for advanced browser automation
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Network interception
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

logger = logging.getLogger(__name__)

@dataclass
class GatedAPIConfig:
    """Configuration for accessing gated APIs"""
    login_url: str
    username_field: str
    password_field: str
    submit_button: str
    success_indicator: str
    wait_time: int = 5
    additional_headers: Optional[Dict[str, str]] = None

@dataclass
class NetworkRequest:
    """Represents a captured network request"""
    url: str
    method: str
    headers: Dict[str, str]
    body: Optional[str] = None
    response_status: Optional[int] = None
    response_headers: Optional[Dict[str, str]] = None
    response_body: Optional[str] = None
    timestamp: float = 0.0

class AdvancedExtractor:
    """Advanced extractor for gated APIs and protected content"""
    
    def __init__(self, headless: bool = True, enable_network_logging: bool = True):
        self.headless = headless
        self.enable_network_logging = enable_network_logging
        self.driver = None
        self.network_requests: List[NetworkRequest] = []
        self.captured_responses: Dict[str, Any] = {}
        
    def setup_driver(self, proxy: Optional[str] = None, user_agent: Optional[str] = None) -> webdriver.Chrome:
        """Setup Chrome driver with advanced capabilities"""
        options = Options()
        
        if self.headless:
            options.add_argument("--headless")
        
        # Performance and stability options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")  # Faster loading
        
        # Network logging capabilities
        if self.enable_network_logging:
            caps = DesiredCapabilities.CHROME
            caps['goog:loggingPrefs'] = {'performance': 'ALL'}
            options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        
        # Custom user agent
        if user_agent:
            options.add_argument(f"--user-agent={user_agent}")
        else:
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Proxy support
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
        
        # Additional capabilities for network interception
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return self.driver
        except Exception as e:
            logger.error(f"Failed to setup Chrome driver: {str(e)}")
            raise
    
    def authenticate_and_access(self, config: GatedAPIConfig, credentials: Dict[str, str]) -> bool:
        """Authenticate and access gated content"""
        try:
            logger.info(f"Attempting to authenticate at: {config.login_url}")
            
            # Navigate to login page
            self.driver.get(config.login_url)
            time.sleep(2)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Fill in credentials
            if config.username_field in credentials:
                username_elem = self.driver.find_element(By.NAME, config.username_field)
                username_elem.clear()
                username_elem.send_keys(credentials[config.username_field])
            
            if config.password_field in credentials:
                password_elem = self.driver.find_element(By.NAME, config.password_field)
                password_elem.clear()
                password_elem.send_keys(credentials[config.password_field])
            
            # Submit form
            submit_elem = self.driver.find_element(By.CSS_SELECTOR, config.submit_button)
            submit_elem.click()
            
            # Wait for authentication
            time.sleep(config.wait_time)
            
            # Check if authentication was successful
            if config.success_indicator:
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, config.success_indicator))
                    )
                    logger.info("Authentication successful")
                    return True
                except:
                    logger.warning("Authentication success indicator not found")
            
            # Alternative success check - check if we're redirected away from login
            current_url = self.driver.current_url
            if "login" not in current_url.lower() and "signin" not in current_url.lower():
                logger.info("Authentication appears successful (redirected from login)")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return False
    
    def capture_network_requests(self, duration: int = 30) -> List[NetworkRequest]:
        """Capture network requests during a specified duration"""
        if not self.enable_network_logging:
            logger.warning("Network logging not enabled")
            return []
        
        logger.info(f"Capturing network requests for {duration} seconds...")
        
        # Clear previous logs
        self.driver.get_log('performance')
        
        # Wait for specified duration
        time.sleep(duration)
        
        # Get performance logs
        logs = self.driver.get_log('performance')
        
        # Parse network requests
        for log in logs:
            try:
                message = json.loads(log['message'])
                if 'message' in message:
                    msg = message['message']
                    
                    if msg['method'] == 'Network.requestWillBeSent':
                        request = NetworkRequest(
                            url=msg['params']['request']['url'],
                            method=msg['params']['request']['method'],
                            headers=msg['params']['request']['headers'],
                            body=msg['params']['request'].get('postData'),
                            timestamp=time.time()
                        )
                        self.network_requests.append(request)
                    
                    elif msg['method'] == 'Network.responseReceived':
                        # Find matching request and update with response info
                        for req in self.network_requests:
                            if req.url == msg['params']['response']['url']:
                                req.response_status = msg['params']['response']['status']
                                req.response_headers = msg['params']['response']['headers']
                                break
                    
                    elif msg['method'] == 'Network.responseReceivedExtraInfo':
                        # Additional response information
                        pass
                        
            except Exception as e:
                logger.debug(f"Failed to parse log entry: {str(e)}")
        
        logger.info(f"Captured {len(self.network_requests)} network requests")
        return self.network_requests
    
    def extract_from_gated_api(self, url: str, config: GatedAPIConfig, 
                              credentials: Dict[str, str], 
                              target_selectors: List[str] = None) -> Dict[str, Any]:
        """Extract API details from a gated/protected API"""
        try:
            logger.info(f"Extracting from gated API: {url}")
            
            # Setup driver if not already done
            if not self.driver:
                self.setup_driver()
            
            # Authenticate first
            if not self.authenticate_and_access(config, credentials):
                raise Exception("Authentication failed")
            
            # Navigate to target URL
            self.driver.get(url)
            time.sleep(3)
            
            # Wait for page to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Capture network requests
            self.capture_network_requests(duration=20)
            
            # Extract visible content
            page_source = self.driver.page_source
            
            # Extract from specific selectors if provided
            extracted_data = {}
            if target_selectors:
                for selector in target_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        extracted_data[selector] = [elem.text for elem in elements]
                    except Exception as e:
                        logger.warning(f"Failed to extract from selector {selector}: {str(e)}")
            
            # Analyze network requests for API patterns
            api_endpoints = self._analyze_network_requests()
            
            # Extract JavaScript and other content
            javascript_data = self._extract_javascript_from_page()
            
            # Get cookies and session data
            cookies = self.driver.get_cookies()
            local_storage = self.driver.execute_script("return Object.keys(localStorage).reduce((obj, key) => { obj[key] = localStorage.getItem(key); return obj; }, {});")
            session_storage = self.driver.execute_script("return Object.keys(sessionStorage).reduce((obj, key) => { obj[key] = sessionStorage.getItem(key); return obj; }, {});")
            
            results = {
                "source_url": url,
                "authentication_status": "success",
                "api_endpoints": api_endpoints,
                "network_requests": [req.__dict__ for req in self.network_requests],
                "javascript_data": javascript_data,
                "cookies": cookies,
                "local_storage": local_storage,
                "session_storage": session_storage,
                "extracted_data": extracted_data,
                "page_source": page_source[:10000],  # First 10KB for analysis
                "timestamp": time.time()
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to extract from gated API {url}: {str(e)}")
            raise
    
    def _analyze_network_requests(self) -> List[Dict[str, Any]]:
        """Analyze captured network requests for API patterns"""
        api_endpoints = []
        
        for request in self.network_requests:
            # Check if this looks like an API call
            if self._is_api_request(request):
                endpoint = {
                    "url": request.url,
                    "method": request.method,
                    "headers": request.headers,
                    "body": request.body,
                    "response_status": request.response_status,
                    "response_headers": request.response_headers,
                    "timestamp": request.timestamp,
                    "confidence": self._calculate_api_confidence(request)
                }
                api_endpoints.append(endpoint)
        
        return api_endpoints
    
    def _is_api_request(self, request: NetworkRequest) -> bool:
        """Determine if a network request is an API call"""
        url = request.url.lower()
        
        # Common API patterns
        api_patterns = [
            '/api/', '/rest/', '/v1/', '/v2/', '/v3/',
            '/graphql', '/swagger', '/openapi',
            'json', 'xml', 'soap'
        ]
        
        # Check URL patterns
        if any(pattern in url for pattern in api_patterns):
            return True
        
        # Check content type headers
        if 'content-type' in request.headers:
            content_type = request.headers['content-type'].lower()
            if 'application/json' in content_type or 'application/xml' in content_type:
                return True
        
        # Check response status (successful API calls)
        if request.response_status and 200 <= request.response_status < 300:
            return True
        
        return False
    
    def _calculate_api_confidence(self, request: NetworkRequest) -> float:
        """Calculate confidence score for API endpoint detection"""
        confidence = 0.0
        
        # URL patterns
        url = request.url.lower()
        if '/api/' in url:
            confidence += 0.4
        if '/rest/' in url:
            confidence += 0.3
        if '/v1/' in url or '/v2/' in url:
            confidence += 0.2
        
        # Content type
        if 'content-type' in request.headers:
            content_type = request.headers['content-type'].lower()
            if 'application/json' in content_type:
                confidence += 0.3
            if 'application/xml' in content_type:
                confidence += 0.2
        
        # Response status
        if request.response_status:
            if 200 <= request.response_status < 300:
                confidence += 0.2
            elif request.response_status == 401 or request.response_status == 403:
                confidence += 0.1  # Authentication required
        
        return min(confidence, 1.0)
    
    def _extract_javascript_from_page(self) -> List[Dict[str, Any]]:
        """Extract JavaScript code and API calls from the page"""
        javascript_data = []
        
        try:
            # Find all script tags
            scripts = self.driver.find_elements(By.TAG_NAME, "script")
            
            for script in scripts:
                try:
                    script_content = script.get_attribute("innerHTML")
                    if script_content:
                        js_data = {
                            "type": "inline_script",
                            "content": script_content,
                            "api_calls": self._extract_api_calls_from_js(script_content)
                        }
                        javascript_data.append(js_data)
                except Exception as e:
                    logger.debug(f"Failed to extract script content: {str(e)}")
            
            # Also check for external scripts
            external_scripts = self.driver.find_elements(By.CSS_SELECTOR, "script[src]")
            for script in external_scripts:
                try:
                    src = script.get_attribute("src")
                    js_data = {
                        "type": "external_script",
                        "src": src,
                        "url": src
                    }
                    javascript_data.append(js_data)
                except Exception as e:
                    logger.debug(f"Failed to extract external script: {str(e)}")
                    
        except Exception as e:
            logger.warning(f"Failed to extract JavaScript: {str(e)}")
        
        return javascript_data
    
    def _extract_api_calls_from_js(self, js_content: str) -> List[Dict[str, Any]]:
        """Extract API calls from JavaScript content"""
        import re
        
        api_calls = []
        
        # Common API call patterns
        patterns = [
            (r'fetch\(["\']([^"\']+)["\']', 'fetch'),
            (r'axios\.(get|post|put|delete)\(["\']([^"\']+)["\']', 'axios'),
            (r'\.ajax\([^)]*url:\s*["\']([^"\']+)["\']', 'jquery_ajax'),
            (r'XMLHttpRequest[^}]*open\(["\']([^"\']+)["\']', 'xmlhttprequest'),
            (r'\.get\(["\']([^"\']+)["\']', 'jquery_get'),
            (r'\.post\(["\']([^"\']+)["\']', 'jquery_post')
        ]
        
        for pattern, call_type in patterns:
            matches = re.findall(pattern, js_content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    url = match[1] if len(match) > 1 else match[0]
                else:
                    url = match
                
                api_calls.append({
                    "type": call_type,
                    "url": url,
                    "pattern": pattern
                })
        
        return api_calls
    
    def close(self):
        """Clean up resources"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                logger.warning(f"Failed to close driver: {str(e)}")
            finally:
                self.driver = None
