"""
Tests for the MenuExtractor module
"""

import pytest
from src.app.core.extractor import MenuExtractor


class TestMenuExtractor:
    """Test cases for MenuExtractor class"""
    
    def setup_method(self):
        """Setup method for each test"""
        self.extractor = MenuExtractor()
    
    def test_extractor_initialization(self):
        """Test extractor initialization"""
        assert self.extractor.max_depth == 3
        assert self.extractor.timeout == 30
        assert self.extractor.session is not None
    
    def test_extract_from_content_empty(self):
        """Test extraction from empty content"""
        results = self.extractor.extract_from_content("", "test")
        assert results["source_name"] == "test"
        assert len(results["endpoints"]) == 0
        assert len(results["forms"]) == 0
    
    def test_extract_from_content_with_html(self):
        """Test extraction from HTML content"""
        html_content = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <a href="/api/users">Users API</a>
                <form action="/submit" method="POST">
                    <input name="username" type="text" required>
                    <input name="password" type="password" required>
                </form>
            </body>
        </html>
        """
        
        results = self.extractor.extract_from_content(html_content, "test_html")
        
        assert results["source_name"] == "test_html"
        assert len(results["endpoints"]) > 0
        assert len(results["forms"]) > 0
        assert results["metadata"]["title"] == "Test Page"
    
    def test_extract_endpoints_patterns(self):
        """Test endpoint extraction patterns"""
        from bs4 import BeautifulSoup
        
        html = '<a href="/api/v1/users">Users</a><a href="/rest/products">Products</a>'
        soup = BeautifulSoup(html, 'html.parser')
        
        endpoints = self.extractor._extract_endpoints(soup, "https://example.com")
        
        assert len(endpoints) == 2
        assert any("/api/v1/users" in ep["url"] for ep in endpoints)
        assert any("/rest/products" in ep["url"] for ep in endpoints)
    
    def test_extract_forms(self):
        """Test form extraction"""
        from bs4 import BeautifulSoup
        
        html = '''
        <form action="/login" method="POST">
            <input name="username" type="text" required>
            <input name="password" type="password" required>
            <select name="role">
                <option value="user">User</option>
                <option value="admin">Admin</option>
            </select>
        </form>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        
        forms = self.extractor._extract_forms(soup, "https://example.com")
        
        assert len(forms) == 1
        form = forms[0]
        assert form["action"] == "https://example.com/login"
        assert form["method"] == "POST"
        assert len(form["inputs"]) == 3
    
    def test_extract_javascript(self):
        """Test JavaScript extraction"""
        from bs4 import BeautifulSoup
        
        html = '''
        <script>
            fetch('/api/data')
                .then(response => response.json())
                .then(data => console.log(data));
            
            axios.get('/api/users')
                .then(response => console.log(response.data));
        </script>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        
        js_data = self.extractor._extract_javascript(soup)
        
        assert len(js_data) >= 2
        assert any(js["type"] == "fetch" for js in js_data)
        assert any(js["type"] == "axios" for js in js_data)
    
    def test_extract_api_keys(self):
        """Test API key extraction"""
        from bs4 import BeautifulSoup
        
        html = '''
        <script>
            const apiKey = "sk-1234567890abcdef";
            const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9";
        </script>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        
        api_keys = self.extractor._extract_api_keys(soup)
        
        assert len(api_keys) >= 1
        # Check that keys are truncated for security
        for key in api_keys:
            assert len(key["value"]) <= 13  # Should be truncated
    
    def teardown_method(self):
        """Cleanup after each test"""
        self.extractor.close()


if __name__ == "__main__":
    pytest.main([__file__])
