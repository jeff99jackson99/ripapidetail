"""
Jeff's API Ripper - Main Streamlit Application
Enhanced with automatic GitHub token detection, beautiful theme, and smart URL handling
"""

import streamlit as st
import json
import logging
from pathlib import Path
import sys
import os

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Try multiple import paths for different deployment environments
try:
    # Try direct imports from current directory structure (for Streamlit Cloud)
    from core.extractor import MenuExtractor
    from core.advanced_extractor import AdvancedExtractor
    from core.gated_api_configs import GatedAPIConfigManager
    from core.github_integration import GitHubIntegration
    from core.api_analyzer import APIAnalyzer
    from core.auto_github import AutoGitHubManager
    from core.url_handler import EnhancedURLHandler
    from utils.config import load_config
    from utils.logging import setup_logging
    from utils.theme import apply_custom_page_config, create_beautiful_header, create_beautiful_card, create_beautiful_divider
    MODULES_LOADED = True
except ImportError as e:
    try:
        # Try the original app.* imports (for local development)
        from app.core.extractor import MenuExtractor
        from app.core.advanced_extractor import AdvancedExtractor
        from app.core.gated_api_configs import GatedAPIConfigManager
        from app.core.github_integration import GitHubIntegration
        from app.core.api_analyzer import APIAnalyzer
        from app.core.auto_github import AutoGitHubManager
        from app.core.url_handler import EnhancedURLHandler
        from app.utils.config import load_config
        from app.utils.logging import setup_logging
        from app.utils.theme import apply_custom_page_config, create_beautiful_header, create_beautiful_card, create_beautiful_divider
        MODULES_LOADED = True
    except ImportError as e2:
        try:
            # Try src.app.* imports (alternative path structure)
            from src.app.core.extractor import MenuExtractor
            from src.app.core.advanced_extractor import AdvancedExtractor
            from src.app.core.gated_api_configs import GatedAPIConfigManager
            from src.app.core.github_integration import GitHubIntegration
            from src.app.core.api_analyzer import APIAnalyzer
            from src.app.core.auto_github import AutoGitHubManager
            from src.app.core.url_handler import EnhancedURLHandler
            from src.app.utils.config import load_config
            from src.app.utils.logging import setup_logging
            from src.app.utils.theme import apply_custom_page_config, create_beautiful_header, create_beautiful_card, create_beautiful_divider
            MODULES_LOADED = True
        except ImportError as e3:
            st.error(f"All import attempts failed. Please check the deployment structure.")
            st.error(f"Error 1: {str(e)}")
            st.error(f"Error 2: {str(e2)}")
            st.error(f"Error 3: {str(e3)}")
            MODULES_LOADED = False

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

def main():
    """Main Streamlit application"""
    
    # Check if modules are available first
    if not MODULES_LOADED:
        st.set_page_config(
            page_title="Jeff's API Ripper",
            page_icon="🔍",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        st.error("⚠️ Some modules failed to load. Basic functionality only.")
        st.info("Please check the deployment logs for more details.")
        
        # Show basic functionality
        show_basic_extraction()
        return
    
    # Apply beautiful theme and page config
    apply_custom_page_config()
    
    # Create beautiful header
    create_beautiful_header(
        "Jeff's API Ripper",
        "Dealer Menu API Details Extractor with Advanced Authentication Support",
        "🔍"
    )
    
    # Initialize automatic GitHub token manager
    auto_github = AutoGitHubManager()
    
    # Try to auto-detect GitHub token
    if not auto_github.token:
        auto_github.auto_detect_token()
    
    # Load configuration
    config = load_config()
    
    # Initialize components
    github_integration = GitHubIntegration(auto_github.token)
    extractor = MenuExtractor(
        max_depth=config.get("max_depth", 3),
        timeout=config.get("timeout", 30)
    )
    advanced_extractor = AdvancedExtractor(
        headless=config.get("selenium_enabled", False),
        enable_network_logging=True
    )
    config_manager = GatedAPIConfigManager()
    analyzer = APIAnalyzer()
    url_handler = EnhancedURLHandler()
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Settings")
        
        # GitHub Token Status
        if auto_github.is_available():
            token_info = auto_github.get_token_info()
            st.success(f"✅ GitHub Token: {token_info['token']}")
            st.info(f"Source: {token_info['source']}")
            
            if st.button("🔄 Refresh Token"):
                auto_github.auto_detect_token()
                st.rerun()
        else:
            st.info("🔍 Auto-detecting GitHub token...")
            if st.button("🔄 Retry Detection"):
                auto_github.auto_detect_token()
                st.rerun()
        
        # Extraction Settings
        st.subheader("⚙️ Extraction Settings")
        max_depth = st.slider(
            "Maximum Crawl Depth", 
            1, 10, 
            config.get("max_depth", 3),
            help="How many levels deep to follow links from the initial URL. Depth 1 = only the initial page, Depth 2 = initial page + linked pages, etc. Higher depths extract more data but take longer."
        )
        timeout = st.number_input(
            "Request Timeout (seconds)", 
            5, 60, 
            config.get("timeout", 30),
            help="Maximum time to wait for each web page to load"
        )
        
        # Advanced Extraction
        st.subheader("🚀 Advanced Extraction")
        selenium_enabled = st.checkbox("Enable Selenium (for gated APIs)", value=config.get("selenium_enabled", False))
        chrome_driver_path = st.text_input("Chrome Driver Path (optional)", value=config.get("chrome_driver_path", ""))
        
        # Save settings
        if st.button("💾 Save Settings"):
            config.update({
                "max_depth": max_depth,
                "timeout": timeout,
                "selenium_enabled": selenium_enabled,
                "chrome_driver_path": chrome_driver_path
            })
            st.success("Settings saved!")
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Extract", "📊 Analyze", "💾 Export", "ℹ️ About"])
    
    with tab1:
        st.header("🔍 API Details Extraction")
        
        # URL Input Section
        create_beautiful_card(
            """
            **Enter the URL of the dealer menu or API documentation you want to analyze:**
            
            The system will automatically detect if the site requires authentication and recommend the best extraction method.
            """,
            "URL Input",
            "🌐"
        )
        
        # Direct URL input (no dropdown)
        url_input = st.text_input(
            "Enter URL:",
            placeholder="https://example.com/dealer-menu or https://api.example.com/docs",
            help="Enter the full URL of the site you want to analyze"
        )
        
        # URL Analysis and Action Buttons
        if url_input:
            # Analyze the URL
            with st.spinner("🔍 Analyzing URL..."):
                try:
                    url_analysis = url_handler.analyze_url(url_input)
                    
                    # Display URL analysis results
                    if url_analysis.get("accessible"):
                        st.success("✅ URL is accessible!")
                        
                        # Show analysis summary
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Status", f"HTTP {url_analysis.get('status_code', 'N/A')}")
                        with col2:
                            st.metric("Auth Required", "Yes" if url_analysis.get("auth_required") else "No")
                        with col3:
                            st.metric("Redirected", "Yes" if url_analysis.get("redirected") else "No")
                        
                        # Show recommendations
                        if url_analysis.get("recommendations"):
                            st.subheader("📋 Recommendations")
                            for rec in url_analysis["recommendations"]:
                                st.info(f"💡 {rec}")
                        
                        # Show detected API endpoints
                        if url_analysis.get("api_endpoints"):
                            st.subheader("🔗 Detected API Endpoints")
                            for endpoint in url_analysis["api_endpoints"][:5]:  # Show first 5
                                st.write(f"• **{endpoint['type']}**: {endpoint['url']}")
                        
                        # Action buttons based on analysis
                        st.subheader("🚀 Choose Extraction Method")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if st.button("🌐 Extract from Public URL", type="primary", use_container_width=True):
                                extract_from_public_url(url_input, extractor, analyzer)
                        
                        with col2:
                            if st.button("🔐 Extract from Gated API", type="primary", use_container_width=True):
                                if url_analysis.get("auth_required"):
                                    # Create auth config suggestion
                                    auth_suggestion = url_handler.create_auth_config_suggestion(url_analysis)
                                    extract_gated_api_details(advanced_extractor, config_manager, url_input, auth_suggestion)
                                else:
                                    st.warning("This URL doesn't appear to require authentication. Use the public URL extraction method instead.")
                        
                        # Show authentication form analysis if available
                        if url_analysis.get("auth_methods"):
                            st.subheader("🔍 Authentication Form Analysis")
                            for i, form in enumerate(url_analysis["auth_methods"][:3]):  # Show first 3
                                with st.expander(f"Form {i+1} (Auth Likelihood: {form['auth_likelihood']:.1%})"):
                                    st.write(f"**Action:** {form['action']}")
                                    st.write(f"**Method:** {form['method']}")
                                    st.write(f"**Fields:** {len(form['fields'])}")
                                    
                                    # Show field details
                                    for field in form['fields']:
                                        field_type = field['type']
                                        field_name = field['name']
                                        if field_type == 'password':
                                            st.write(f"🔒 **Password Field:** {field_name}")
                                        elif field_type in ['text', 'email']:
                                            st.write(f"👤 **Username Field:** {field_name}")
                                        elif field_type == 'submit':
                                            st.write(f"📤 **Submit Button:** {field_name}")
                    
                    else:
                        st.error("❌ URL is not accessible")
                        st.error(f"Error: {url_analysis.get('error', 'Unknown error')}")
                        st.info("💡 Please check the URL and try again")
                        
                except Exception as e:
                    st.error(f"URL analysis failed: {str(e)}")
                    st.info("Proceeding with basic extraction...")
        
        # File Upload Option
        create_beautiful_divider()
        st.subheader("📁 Alternative: File Upload")
        
        uploaded_file = st.file_uploader(
            "Upload HTML file or text content:",
            type=['html', 'htm', 'txt'],
            help="Upload a local file instead of providing a URL"
        )
        
        if uploaded_file:
            if st.button("📄 Extract from File", type="primary"):
                content = uploaded_file.read().decode('utf-8')
                extract_from_content(content, extractor, analyzer)
    
    with tab2:
        st.header("📊 Analysis Results")
        
        if 'extraction_results' in st.session_state:
            display_analysis_results(st.session_state.extraction_results, analyzer)
        else:
            st.info("🔍 No extraction results to analyze. Please extract data first.")
    
    with tab3:
        st.header("💾 Export Results")
        
        if 'extraction_results' in st.session_state:
            export_results(st.session_state.extraction_results)
        else:
            st.info("📤 No results to export. Please extract data first.")
    
    with tab4:
        st.header("ℹ️ About Jeff's API Ripper")
        
        create_beautiful_card(
            """
            **Jeff's API Ripper** is a powerful tool designed to extract API details from dealer menus and other web sources.
            
            **Features:**
            • 🔍 **Smart URL Analysis** - Automatically detects password protection and authentication requirements
            • 🔐 **Gated API Support** - Extract from protected APIs using browser automation
            • 🌐 **Public Site Extraction** - Extract from publicly accessible websites
            • 🤖 **Automatic GitHub Integration** - No need to manually enter tokens
            • 🎨 **Beautiful Modern UI** - Clean, responsive interface with gradient themes
            • 📊 **Comprehensive Analysis** - Detailed API endpoint and form analysis
            • 💾 **Multiple Export Formats** - JSON, CSV, and API documentation
            
            **Perfect for:**
            • Dealer menu API integration
            • API documentation extraction
            • Web scraping and data extraction
            • Authentication flow analysis
            """,
            "About",
            "ℹ️"
        )

def extract_from_public_url(url: str, extractor: MenuExtractor, analyzer: APIAnalyzer):
    """Extract API details from a public URL"""
    with st.spinner("🔍 Extracting API details..."):
        try:
            results = extractor.extract_from_url(url)
            
            # Store results in session state
            st.session_state.extraction_results = results
            
            st.success("🎉 Extraction completed successfully!")
            
            # Display results
            display_extraction_results(results)
            
        except Exception as e:
            st.error(f"❌ Extraction failed: {str(e)}")
            logger.error(f"URL extraction failed: {str(e)}")

def extract_from_content(content: str, extractor: MenuExtractor, analyzer: APIAnalyzer):
    """Extract API details from content"""
    with st.spinner("🔍 Extracting API details from content..."):
        try:
            results = extractor.extract_from_content(content)
            
            # Store results in session state
            st.session_state.extraction_results = results
            
            st.success("🎉 Extraction completed successfully!")
            
            # Display results
            display_extraction_results(results)
            
        except Exception as e:
            st.error(f"❌ Extraction failed: {str(e)}")
            logger.error(f"Content extraction failed: {str(e)}")

def extract_gated_api_details(advanced_extractor: AdvancedExtractor, config_manager: GatedAPIConfigManager, target_url: str = "", auth_suggestion: dict = None):
    """Extract API details from gated/protected APIs"""
    st.header("🔐 Gated API Extraction")
    st.markdown("Extract API details from protected APIs that require authentication")
    
    # Configuration selection
    st.subheader("1. Select API Configuration")
    
    # Get available configurations
    available_configs = config_manager.list_configs()
    selected_config = st.selectbox(
        "Choose API Platform",
        available_configs,
        help="Select a predefined configuration or create a custom one"
    )
    
    # Show configuration details
    config_info = config_manager.get_config_info(selected_config)
    
    with st.expander(f"Configuration Details: {config_info['name']}"):
        st.write(f"**Description:** {config_info['description']}")
        st.write(f"**Login URL:** {config_info['login_url']}")
        st.write(f"**Username Field:** {config_info['username_field']}")
        st.write(f"**Password Field:** {config_info['password_field']}")
        st.write(f"**Submit Button:** {config_info['submit_button']}")
        st.write(f"**Success Indicator:** {config_info['success_indicator']}")
        st.write(f"**Target Selectors:** {', '.join(config_info['target_selectors'])}")
        st.write(f"**Notes:** {config_info['notes']}")
    
    # Show auth suggestion if available
    if auth_suggestion:
        st.subheader("🔍 Authentication Suggestion")
        st.info("Based on URL analysis, we suggest the following configuration:")
        st.json(auth_suggestion)
        
        # Auto-fill fields if suggestion is available
        if auth_suggestion.get("username_field"):
            config_info['username_field'] = auth_suggestion['username_field']
        if auth_suggestion.get("password_field"):
            config_info['password_field'] = auth_suggestion['password_field']
        if auth_suggestion.get("submit_button"):
            config_info['submit_button'] = auth_suggestion['submit_button']
    
    # Credentials input
    st.subheader("2. Enter Credentials")
    
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input(
            "Username/Email",
            value=config_info['example_credentials'].get('username', ''),
            help="Enter your username or email for the selected platform"
        )
    
    with col2:
        password = st.text_input(
            "Password",
            type="password",
            help="Enter your password for the selected platform"
        )
    
    # Target URL
    st.subheader("3. Target URL")
    target_url_input = st.text_input(
        "URL to Extract From",
        value=target_url,
        help="Enter the URL of the page containing the API documentation"
    )
    
    # Advanced options
    st.subheader("4. Advanced Options")
    
    col1, col2 = st.columns(2)
    with col1:
        capture_duration = st.slider(
            "Network Capture Duration (seconds)",
            min_value=10,
            max_value=60,
            value=20,
            help="How long to capture network requests"
        )
    
    with col2:
        headless_mode = st.checkbox(
            "Headless Mode",
            value=True,
            help="Run browser in background (recommended for production)"
        )
    
    # Custom selectors
    custom_selectors = st.text_area(
        "Custom CSS Selectors (optional)",
        value="\n".join(config_info['target_selectors']),
        help="Additional CSS selectors to extract content from. One per line."
    )
    
    # Extract button
    if st.button("🔍 Extract from Gated API", type="primary"):
        if not username or not password or not target_url_input:
            st.error("Please fill in all required fields: username, password, and target URL")
            return
        
        if not config_info['login_url']:
            st.error("Selected configuration is missing login URL. Please choose a valid configuration or create a custom one.")
            return
        
        # Prepare for extraction
        with st.spinner("Setting up advanced extraction..."):
            try:
                # Update extractor settings
                advanced_extractor.headless = headless_mode
                
                # Parse custom selectors
                target_selectors = [s.strip() for s in custom_selectors.split('\n') if s.strip()]
                
                # Prepare credentials
                credentials = {
                    config_info['username_field']: username,
                    config_info['password_field']: password
                }
                
                # Get the configuration
                config = config_manager.get_config(selected_config).config
                
                # Update configuration with custom values if needed
                if selected_config == "custom":
                    config.login_url = st.text_input("Login URL", value="")
                    config.username_field = st.text_input("Username Field Name", value="username")
                    config.password_field = st.text_input("Password Field Name", value="password")
                    config.submit_button = st.text_input("Submit Button Selector", value="button[type='submit']")
                    config.success_indicator = st.text_input("Success Indicator Selector", value="")
                
                st.success("Setup complete! Starting extraction...")
                
            except Exception as e:
                st.error(f"Setup failed: {str(e)}")
                return
        
        # Perform extraction
        with st.spinner("Authenticating and extracting API details..."):
            try:
                # Setup driver
                advanced_extractor.setup_driver()
                
                # Perform extraction
                results = advanced_extractor.extract_from_gated_api(
                    url=target_url_input,
                    config=config,
                    credentials=credentials,
                    target_selectors=target_selectors
                )
                
                # Store results in session state
                st.session_state.extraction_results = results
                
                st.success("🎉 Gated API extraction completed successfully!")
                
                # Display results
                display_gated_api_results(results)
                
            except Exception as e:
                st.error(f"Extraction failed: {str(e)}")
                st.error("This could be due to:")
                st.error("• Invalid credentials")
                st.error("• Changed login page structure")
                st.error("• Network connectivity issues")
                st.error("• Anti-bot protection")
                
            finally:
                # Cleanup
                advanced_extractor.close()

def display_extraction_results(results: dict):
    """Display the results from standard extraction"""
    st.subheader("📊 Extraction Results")
    
    if not results:
        st.warning("No results to display")
        return
    
    # API Endpoints
    if results.get("api_endpoints"):
        st.write(f"**🌐 API Endpoints Found: {len(results['api_endpoints'])}**")
        
        for i, endpoint in enumerate(results["api_endpoints"]):
            with st.expander(f"Endpoint {i+1}: {endpoint.get('method', 'N/A')} {endpoint.get('url', 'N/A')}"):
                st.json(endpoint)
    
    # Forms
    if results.get("forms"):
        st.write(f"**📝 Forms Found: {len(results['forms'])}**")
        
        for i, form in enumerate(results["forms"]):
            with st.expander(f"Form {i+1}: {form.get('action', 'N/A')}"):
                st.json(form)
    
    # JavaScript
    if results.get("javascript"):
        st.write(f"**⚡ JavaScript Found: {len(results['javascript'])}**")
        
        for i, js in enumerate(results["javascript"][:5]):  # Show first 5
            with st.expander(f"Script {i+1}: {js.get('type', 'N/A')}"):
                st.json(js)
    
    # API Keys
    if results.get("api_keys"):
        st.write(f"**🔑 API Keys Found: {len(results['api_keys'])}**")
        
        for i, key in enumerate(results["api_keys"]):
            with st.expander(f"API Key {i+1}"):
                st.json(key)

def display_gated_api_results(results: dict):
    """Display the results from gated API extraction"""
    st.subheader("🔓 Extracted API Details")
    
    if not results:
        st.warning("No results to display")
        return
    
    # Authentication status
    auth_status = results.get("authentication_status", "unknown")
    st.write(f"**Authentication Status:** {auth_status}")
    
    # API Endpoints
    if results.get("api_endpoints"):
        st.write(f"**🌐 API Endpoints Found: {len(results['api_endpoints'])}**")
        
        for i, endpoint in enumerate(results["api_endpoints"]):
            with st.expander(f"Endpoint {i+1}: {endpoint.get('method', 'N/A')} {endpoint.get('url', 'N/A')}"):
                st.json(endpoint)
    
    # Network Requests
    if results.get("network_requests"):
        st.write(f"**📡 Network Requests Captured: {len(results['network_requests'])}**")
        
        # Filter for API-like requests
        api_requests = [req for req in results["network_requests"] 
                       if any(pattern in req.get('url', '').lower() 
                             for pattern in ['/api/', '/rest/', '/v1/', '/v2/', 'json', 'xml'])]
        
        if api_requests:
            st.write(f"**🔍 API-like Requests: {len(api_requests)}**")
            for req in api_requests[:10]:  # Show first 10
                with st.expander(f"Request: {req.get('method', 'N/A')} {req.get('url', 'N/A')}"):
                    st.json(req)
    
    # JavaScript Data
    if results.get("javascript_data"):
        st.write(f"**⚡ JavaScript Analysis: {len(results['javascript_data'])} scripts found**")
        
        for i, js in enumerate(results["javascript_data"][:5]):  # Show first 5
            with st.expander(f"Script {i+1}: {js.get('type', 'N/A')}"):
                if js.get('api_calls'):
                    st.write(f"**API Calls Found: {len(js['api_calls'])}**")
                    for call in js['api_calls']:
                        st.write(f"• {call.get('type', 'N/A')}: {call.get('url', 'N/A')}")
                else:
                    st.write("No API calls detected in this script")
    
    # Session Data
    if results.get("cookies") or results.get("local_storage") or results.get("session_storage"):
        st.write("**🍪 Session Information**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if results.get("cookies"):
                st.write(f"**Cookies:** {len(results['cookies'])}")
                with st.expander("View Cookies"):
                    for cookie in results['cookies'][:5]:  # Show first 5
                        st.write(f"• {cookie.get('name', 'N/A')}: {cookie.get('value', 'N/A')[:50]}...")
        
        with col2:
            if results.get("local_storage"):
                st.write(f"**Local Storage:** {len(results['local_storage'])}")
                with st.expander("View Local Storage"):
                    for key, value in list(results['local_storage'].items())[:5]:
                        st.write(f"• {key}: {str(value)[:50]}...")
        
        with col3:
            if results.get("session_storage"):
                st.write(f"**Session Storage:** {len(results['session_storage'])}")
                with st.expander("View Session Storage"):
                    for key, value in list(results['session_storage'].items())[:5]:
                        st.write(f"• {key}: {str(value)[:50]}...")
    
    # Extracted Data
    if results.get("extracted_data"):
        st.write("**📄 Content Extraction**")
        for selector, content in results["extracted_data"].items():
            with st.expander(f"Selector: {selector}"):
                if isinstance(content, list):
                    for i, item in enumerate(content[:3]):  # Show first 3
                        st.write(f"{i+1}. {item[:200]}...")
                else:
                    st.write(str(content)[:500] + "...")

def display_analysis_results(results: dict, analyzer: APIAnalyzer):
    """Display analysis results"""
    st.subheader("📊 Analysis Results")
    
    # Analyze the results
    analysis = analyzer.analyze_all(results)
    
    # Display analysis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Endpoints", len(results.get("api_endpoints", [])))
    
    with col2:
        st.metric("Security Issues", len(analysis.get("security_concerns", [])))
    
    with col3:
        st.metric("Recommendations", len(analysis.get("recommendations", [])))
    
    # Security concerns
    if analysis.get("security_concerns"):
        st.subheader("⚠️ Security Concerns")
        for concern in analysis["security_concerns"]:
            st.warning(concern)
    
    # Recommendations
    if analysis.get("recommendations"):
        st.subheader("💡 Recommendations")
        for rec in analysis["recommendations"]:
            st.info(rec)
    
    # API patterns
    if analysis.get("api_patterns"):
        st.subheader("🔍 API Patterns")
        for pattern in analysis["api_patterns"]:
            st.write(f"• **{pattern['type']}**: {pattern['description']}")

def export_results(results: dict):
    """Export results in various formats"""
    st.subheader("💾 Export Results")
    
    # JSON export
    if st.button("📄 Export as JSON"):
        json_str = json.dumps(results, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name="api_extraction_results.json",
            mime="application/json"
        )
    
    # CSV export
    if st.button("📊 Export as CSV"):
        # Convert results to CSV format
        csv_data = convert_to_csv(results)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name="api_extraction_results.csv",
            mime="text/csv"
        )
    
    # API documentation export
    if st.button("📚 Export as API Docs"):
        docs = generate_api_documentation(results)
        st.download_button(
            label="📥 Download API Docs",
            data=docs,
            file_name="api_documentation.md",
            mime="text/markdown"
        )

def convert_to_csv(results: dict) -> str:
    """Convert results to CSV format"""
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow(["Type", "URL", "Method", "Description"])
    
    # Write API endpoints
    for endpoint in results.get("api_endpoints", []):
        writer.writerow([
            "API Endpoint",
            endpoint.get("url", ""),
            endpoint.get("method", ""),
            endpoint.get("description", "")
        ])
    
    # Write forms
    for form in results.get("forms", []):
        writer.writerow([
            "Form",
            form.get("action", ""),
            form.get("method", ""),
            f"Fields: {len(form.get('fields', []))}"
        ])
    
    return output.getvalue()

def generate_api_documentation(results: dict) -> str:
    """Generate API documentation in Markdown format"""
    docs = "# API Documentation\n\n"
    docs += f"Generated by Jeff's API Ripper on {results.get('timestamp', 'Unknown')}\n\n"
    
    # API Endpoints
    if results.get("api_endpoints"):
        docs += "## API Endpoints\n\n"
        for endpoint in results["api_endpoints"]:
            docs += f"### {endpoint.get('method', 'GET')} {endpoint.get('url', '')}\n\n"
            if endpoint.get("description"):
                docs += f"{endpoint['description']}\n\n"
            if endpoint.get("parameters"):
                docs += "**Parameters:**\n"
                for param in endpoint["parameters"]:
                    docs += f"- {param.get('name', '')}: {param.get('type', '')}\n"
                docs += "\n"
    
    # Forms
    if results.get("forms"):
        docs += "## Forms\n\n"
        for form in results["forms"]:
            docs += f"### Form: {form.get('action', '')}\n\n"
            docs += f"**Method:** {form.get('method', 'GET')}\n\n"
            if form.get("fields"):
                docs += "**Fields:**\n"
                for field in form["fields"]:
                    docs += f"- {field.get('name', '')} ({field.get('type', 'text')})\n"
                docs += "\n"
    
    return docs

def show_basic_extraction():
    """Show basic extraction functionality when advanced modules fail"""
    st.header("🔍 Basic API Details Extraction")
    
    # URL Input
    url_input = st.text_input(
        "Enter URL:",
        placeholder="https://example.com/dealer-menu",
        help="Enter the full URL of the site you want to analyze"
    )
    
    if url_input:
        st.info(f"URL entered: {url_input}")
        st.warning("Advanced extraction features are not available. Please check the deployment logs.")
    
    # File Upload
    st.subheader("📁 File Upload")
    uploaded_file = st.file_uploader(
        "Upload HTML file or text content:",
        type=['html', 'htm', 'txt'],
        help="Upload a local file instead of providing a URL"
    )
    
    if uploaded_file:
        st.info(f"File uploaded: {uploaded_file.name}")
        st.warning("File processing features are not available. Please check the deployment logs.")

if __name__ == "__main__":
    main()
