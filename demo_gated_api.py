#!/usr/bin/env python3
"""
Demo script for Jeff's API Ripper - Gated API Extraction
This script demonstrates the advanced extraction capabilities for protected APIs
"""

import sys
from pathlib import Path
import json
import time

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from app.core.advanced_extractor import AdvancedExtractor, GatedAPIConfig
from app.core.gated_api_configs import GatedAPIConfigManager

def demo_gated_api_extraction():
    """Demonstrate gated API extraction functionality"""
    print("🔐 Jeff's API Ripper - Gated API Demo")
    print("=" * 60)
    print("This demo shows how to extract API details from protected/gated APIs")
    print()
    
    # Initialize components
    config_manager = GatedAPIConfigManager()
    
    # Show available configurations
    print("📋 Available API Configurations:")
    available_configs = config_manager.list_configs()
    for i, config_name in enumerate(available_configs, 1):
        config_info = config_manager.get_config_info(config_name)
        print(f"  {i}. {config_info['name']} - {config_info['description']}")
    
    print()
    
    # Demo with a specific configuration
    print("🎯 Demo Configuration: Stripe")
    stripe_config = config_manager.get_config("stripe")
    
    print(f"Platform: {stripe_config.name}")
    print(f"Description: {stripe_config.description}")
    print(f"Login URL: {stripe_config.config.login_url}")
    print(f"Username Field: {stripe_config.config.username_field}")
    print(f"Password Field: {stripe_config.config.password_field}")
    print(f"Submit Button: {stripe_config.config.submit_button}")
    print(f"Success Indicator: {stripe_config.config.success_indicator}")
    print(f"Target Selectors: {', '.join(stripe_config.target_selectors)}")
    print(f"Notes: {stripe_config.notes}")
    
    print()
    print("🔑 Example Credentials:")
    for field, value in stripe_config.example_credentials.items():
        print(f"  {field}: {value}")
    
    print()
    print("📡 What This Demo Would Extract:")
    print("  • API endpoints from Stripe's developer dashboard")
    print("  • Network requests during API documentation browsing")
    print("  • JavaScript API calls and examples")
    print("  • Authentication tokens and session data")
    print("  • API documentation content")
    print("  • Request/response examples")
    
    print()
    print("⚙️ Advanced Features:")
    print("  • Browser automation with Selenium")
    print("  • Network request interception")
    print("  • JavaScript execution and analysis")
    print("  • Session management and cookie handling")
    print("  • Custom CSS selector targeting")
    print("  • Headless browser support")
    
    print()
    print("🚀 To Use This Feature:")
    print("  1. Run the Streamlit app: streamlit run src/app/main.py")
    print("  2. Select 'Gated API' as source type")
    print("  3. Choose your target platform")
    print("  4. Enter your credentials")
    print("  5. Specify the target URL")
    print("  6. Click 'Extract from Gated API'")
    
    print()
    print("⚠️  Important Notes:")
    print("  • Only use with your own accounts or authorized access")
    print("  • Respect rate limits and terms of service")
    print("  • Some platforms may have anti-bot protection")
    print("  • Chrome/Chromium browser required for Selenium")
    
    print()
    print("🔧 Technical Requirements:")
    print("  • Python 3.11+")
    print("  • Chrome/Chromium browser")
    print("  • ChromeDriver (auto-downloaded)")
    print("  • Selenium WebDriver")
    print("  • Network access to target platforms")

def demo_custom_config_creation():
    """Demonstrate custom configuration creation"""
    print("\n" + "=" * 60)
    print("🛠️  Custom Configuration Creation Demo")
    print("=" * 60)
    
    config_manager = GatedAPIConfigManager()
    
    # Example custom configuration
    print("📝 Example: Creating a custom configuration for 'MyCompany API'")
    
    custom_key = config_manager.create_custom_config(
        name="MyCompany API",
        login_url="https://api.mycompany.com/login",
        username_field="email",
        password_field="password",
        submit_button="button[type='submit']",
        success_indicator=".dashboard-header",
        target_selectors=[
            ".api-docs",
            ".endpoint-list",
            "[data-api]",
            ".swagger-ui"
        ]
    )
    
    print(f"✅ Custom configuration created with key: {custom_key}")
    
    # Show the custom configuration
    custom_config = config_manager.get_config(custom_key)
    print(f"Configuration Name: {custom_config.name}")
    print(f"Login URL: {custom_config.config.login_url}")
    print(f"Target Selectors: {', '.join(custom_config.target_selectors)}")
    
    print()
    print("💡 Custom Configuration Tips:")
    print("  • Use browser developer tools to find field names")
    print("  • CSS selectors should be specific and reliable")
    print("  • Test selectors in browser console first")
    print("  • Consider multiple success indicators")
    print("  • Update configurations when platforms change")

def demo_network_analysis():
    """Demonstrate network analysis capabilities"""
    print("\n" + "=" * 60)
    print("📡 Network Analysis Capabilities")
    print("=" * 60)
    
    print("🔍 What Gets Captured:")
    print("  • All HTTP/HTTPS requests and responses")
    print("  • Request headers and parameters")
    print("  • Response status codes and headers")
    print("  • Request/response bodies")
    print("  • Timing information")
    print("  • API endpoint patterns")
    
    print()
    print("🎯 API Detection Patterns:")
    print("  • URL patterns: /api/, /rest/, /v1/, /v2/")
    print("  • Content types: application/json, application/xml")
    print("  • Response status codes: 200, 201, 400, 401, 403")
    print("  • Authentication headers: Authorization, Bearer")
    print("  • API-specific headers: X-API-Key, X-Client-ID")
    
    print()
    print("📊 Confidence Scoring:")
    print("  • High confidence (0.8-1.0): Clear API patterns")
    print("  • Medium confidence (0.5-0.7): Likely API calls")
    print("  • Low confidence (0.1-0.4): Potential API calls")
    print("  • Factors: URL structure, content type, status codes")

def demo_security_features():
    """Demonstrate security and privacy features"""
    print("\n" + "=" * 60)
    print("🔒 Security and Privacy Features")
    print("=" * 60)
    
    print("🛡️  Built-in Security:")
    print("  • Credential masking in logs")
    print("  • Session isolation per extraction")
    print("  • Automatic cleanup of sensitive data")
    print("  • No persistent storage of credentials")
    print("  • Secure handling of cookies and tokens")
    
    print()
    print("🔐 Authentication Handling:")
    print("  • Support for various login flows")
    print("  • Multi-factor authentication awareness")
    print("  • Session token management")
    print("  • Cookie and header preservation")
    print("  • OAuth flow support")
    
    print()
    print("📋 Privacy Considerations:")
    print("  • Only extract from authorized sources")
    print("  • Respect robots.txt and terms of service")
    print("  • Implement appropriate rate limiting")
    print("  • Handle personal data responsibly")
    print("  • Log minimal information for debugging")

if __name__ == "__main__":
    try:
        demo_gated_api_extraction()
        demo_custom_config_creation()
        demo_network_analysis()
        demo_security_features()
        
        print("\n" + "=" * 60)
        print("🎉 Gated API Demo Completed!")
        print("=" * 60)
        print("\nTo run the full application with gated API support:")
        print("  streamlit run src/app/main.py")
        print("\nFor more information, check the README.md and DEPLOYMENT.md files")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        print("Make sure you have installed the dependencies:")
        print("  pip install -e .")
