#!/usr/bin/env python3
"""
Demo script for Jeff's API Ripper
This script demonstrates the core functionality without the Streamlit interface
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from app.core.extractor import MenuExtractor
from app.core.api_analyzer import APIAnalyzer
from app.utils.config import load_config

def demo_extraction():
    """Demonstrate API extraction functionality"""
    print("🔍 Jeff's API Ripper - Demo Mode")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    
    # Initialize components
    extractor = MenuExtractor(
        max_depth=config.get("max_depth", 3),
        timeout=config.get("timeout", 30)
    )
    analyzer = APIAnalyzer()
    
    # Example HTML content with API details
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sample Dealer Menu</title>
        <meta name="description" content="Car dealership inventory">
    </head>
    <body>
        <h1>Car Dealership</h1>
        
        <!-- API Endpoints -->
        <a href="/api/v1/vehicles">View Vehicles</a>
        <a href="/api/v1/inventory">Check Inventory</a>
        <a href="/rest/customers">Customer Management</a>
        
        <!-- Forms -->
        <form action="/api/v1/search" method="POST">
            <input name="make" type="text" placeholder="Car Make" required>
            <input name="model" type="text" placeholder="Car Model" required>
            <input name="year" type="number" placeholder="Year" min="1900" max="2025">
            <button type="submit">Search</button>
        </form>
        
        <!-- JavaScript API calls -->
        <script>
            // Fetch vehicle data
            fetch('/api/v1/vehicles')
                .then(response => response.json())
                .then(data => console.log('Vehicles:', data));
            
            // Axios call for inventory
            axios.get('/api/v1/inventory')
                .then(response => console.log('Inventory:', response.data));
            
            // API key (for demonstration)
            const apiKey = "sk-demo123456789";
        </script>
    </body>
    </html>
    """
    
    print("\n📄 Extracting API details from sample HTML...")
    
    try:
        # Extract API details
        results = extractor.extract_from_content(sample_html, "demo_sample")
        
        print(f"✅ Extraction completed!")
        print(f"📊 Found {len(results['endpoints'])} API endpoints")
        print(f"📝 Found {len(results['forms'])} forms")
        print(f"🔧 Found {len(results['javascript'])} JavaScript API calls")
        print(f"🔑 Found {len(results['api_keys'])} potential API keys")
        
        # Display endpoints
        if results['endpoints']:
            print("\n🌐 API Endpoints:")
            for i, endpoint in enumerate(results['endpoints'], 1):
                print(f"  {i}. {endpoint['method']} {endpoint['url']}")
                if endpoint['description']:
                    print(f"     Description: {endpoint['description']}")
        
        # Display forms
        if results['forms']:
            print("\n📋 Forms:")
            for i, form in enumerate(results['forms'], 1):
                print(f"  {i}. {form['method']} {form['action']}")
                print(f"     Inputs: {len(form['inputs'])} fields")
        
        # Display JavaScript
        if results['javascript']:
            print("\n⚡ JavaScript API Calls:")
            for i, js in enumerate(results['javascript'], 1):
                print(f"  {i}. {js['type']}: {js['url']}")
        
        # Analyze patterns
        print("\n🔍 Analyzing patterns...")
        analysis = analyzer.analyze_patterns(results)
        
        if analysis['patterns']:
            print("\n📈 Detected Patterns:")
            for pattern in analysis['patterns']:
                print(f"  • {pattern['type']} (confidence: {pattern['confidence']})")
                print(f"    {pattern['description']}")
        
        if analysis['recommendations']:
            print("\n💡 Recommendations:")
            for rec in analysis['recommendations']:
                print(f"  • {rec}")
        
        if analysis['security_concerns']:
            print("\n⚠️  Security Concerns:")
            for concern in analysis['security_concerns']:
                print(f"  • {concern}")
        
        # Generate documentation
        print("\n📚 Generating API documentation...")
        doc = analyzer.generate_api_documentation(results)
        
        # Save documentation to file
        with open("demo_api_documentation.md", "w") as f:
            f.write(doc)
        
        print("✅ API documentation saved to 'demo_api_documentation.md'")
        
    except Exception as e:
        print(f"❌ Error during extraction: {str(e)}")
    
    finally:
        # Cleanup
        extractor.close()

def demo_url_extraction():
    """Demonstrate URL extraction (requires internet connection)"""
    print("\n🌐 Demo URL Extraction")
    print("=" * 30)
    print("Note: This requires an internet connection and a valid URL")
    
    url = input("Enter a URL to extract API details from (or press Enter to skip): ").strip()
    
    if not url:
        print("Skipping URL extraction demo")
        return
    
    try:
        extractor = MenuExtractor()
        print(f"🔍 Extracting from: {url}")
        
        results = extractor.extract_from_url(url)
        
        print(f"✅ Extraction completed!")
        print(f"📊 Found {len(results['endpoints'])} API endpoints")
        print(f"📝 Found {len(results['forms'])} forms")
        print(f"🔧 Found {len(results['javascript'])} JavaScript API calls")
        
        # Save results
        import json
        with open("demo_url_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print("✅ Results saved to 'demo_url_results.json'")
        
    except Exception as e:
        print(f"❌ Error during URL extraction: {str(e)}")
    
    finally:
        extractor.close()

if __name__ == "__main__":
    try:
        demo_extraction()
        demo_url_extraction()
        
        print("\n🎉 Demo completed!")
        print("\nTo run the full Streamlit application:")
        print("  streamlit run src/app/main.py")
        print("\nTo install dependencies:")
        print("  pip install -e .")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        print("Make sure you have installed the dependencies:")
        print("  pip install -e .")
