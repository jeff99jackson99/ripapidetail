"""
API Ripper - Main Streamlit Application
Extracts API details from dealer menus and other sources
"""

import streamlit as st
import asyncio
from pathlib import Path
import sys
import json
import csv
import io

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from app.core.extractor import MenuExtractor
from app.core.github_integration import GitHubIntegration
from app.core.api_analyzer import APIAnalyzer
from app.utils.config import load_config
from app.utils.logging import setup_logging

# Setup logging
logger = setup_logging()

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="API Ripper",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🔍 Jeff's API Ripper - Dealer Menu Extractor")
    st.markdown("Extract API details from dealer menus and other sources")
    
    # Load configuration
    config = load_config()
    
    # Initialize components
    github_integration = GitHubIntegration(config.get("github_token"))
    extractor = MenuExtractor(
        max_depth=config.get("max_depth", 3),
        timeout=config.get("timeout", 30)
    )
    analyzer = APIAnalyzer()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Source type selection
        source_type = st.selectbox(
            "Source Type",
            ["URL", "File Upload", "GitHub Repository", "Direct Input"]
        )
        
        # GitHub integration settings
        if st.checkbox("Enable GitHub Integration"):
            repo_url = st.text_input("GitHub Repository URL")
            branch = st.text_input("Branch", value="main")
            
            if st.button("Sync with GitHub"):
                if repo_url:
                    with st.spinner("Syncing with GitHub..."):
                        try:
                            github_integration.sync_repository(repo_url, branch)
                            st.success("GitHub sync completed!")
                        except Exception as e:
                            st.error(f"GitHub sync failed: {str(e)}")
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs([
        "Extract API Details", 
        "Analyze Results", 
        "Export Data", 
        "Settings"
    ])
    
    with tab1:
        extract_api_details(source_type, extractor)
    
    with tab2:
        analyze_results(analyzer)
    
    with tab3:
        export_data()
    
    with tab4:
        show_settings(config)

def extract_api_details(source_type: str, extractor: MenuExtractor):
    """Extract API details from the selected source"""
    st.header("Extract API Details")
    
    if source_type == "URL":
        url = st.text_input("Enter Dealer Menu URL")
        if st.button("Extract API Details"):
            if url:
                with st.spinner("Extracting API details..."):
                    try:
                        results = extractor.extract_from_url(url)
                        st.session_state.extraction_results = results
                        st.success("Extraction completed!")
                        display_extraction_results(results)
                    except Exception as e:
                        st.error(f"Extraction failed: {str(e)}")
    
    elif source_type == "File Upload":
        uploaded_file = st.file_uploader(
            "Upload HTML/Text file", 
            type=['html', 'htm', 'txt', 'json']
        )
        if uploaded_file and st.button("Extract API Details"):
            with st.spinner("Extracting API details..."):
                try:
                    content = uploaded_file.read().decode('utf-8')
                    results = extractor.extract_from_content(content, uploaded_file.name)
                    st.session_state.extraction_results = results
                    st.success("Extraction completed!")
                    display_extraction_results(results)
                except Exception as e:
                    st.error(f"Extraction failed: {str(e)}")
    
    elif source_type == "GitHub Repository":
        st.info("GitHub repository extraction will be implemented in the next version")
    
    elif source_type == "Direct Input":
        content = st.text_area("Paste HTML/Text content here")
        if st.button("Extract API Details"):
            if content:
                with st.spinner("Extracting API details..."):
                    try:
                        results = extractor.extract_from_content(content, "direct_input")
                        st.session_state.extraction_results = results
                        st.success("Extraction completed!")
                        display_extraction_results(results)
                    except Exception as e:
                        st.error(f"Extraction failed: {str(e)}")

def display_extraction_results(results: dict):
    """Display the extracted API details"""
    st.subheader("Extracted API Details")
    
    if not results:
        st.warning("No results to display")
        return
    
    # Display endpoints
    if results.get("endpoints"):
        st.write("**API Endpoints Found:**")
        for endpoint in results["endpoints"]:
            with st.expander(f"Endpoint: {endpoint.get('url', 'N/A')}"):
                st.json(endpoint)
    
    # Display forms
    if results.get("forms"):
        st.write("**Forms Found:**")
        for form in results["forms"]:
            with st.expander(f"Form: {form.get('action', 'N/A')}"):
                st.json(form)
    
    # Display JavaScript
    if results.get("javascript"):
        st.write("**JavaScript API Calls Found:**")
        for js in results["javascript"]:
            with st.expander(f"JavaScript: {js.get('type', 'N/A')}"):
                st.code(js.get('code', ''), language='javascript')
    
    # Display network requests
    if results.get("network_requests"):
        st.write("**Network Requests Found:**")
        for req in results["network_requests"]:
            with st.expander(f"Request: {req.get('url', 'N/A')}"):
                st.json(req)

def analyze_results(analyzer: APIAnalyzer):
    """Analyze the extracted results"""
    st.header("Analyze Results")
    
    if not hasattr(st.session_state, 'extraction_results'):
        st.info("No extraction results to analyze. Please extract API details first.")
        return
    
    results = st.session_state.extraction_results
    
    # Analyze patterns
    analysis = analyzer.analyze_patterns(results)
    
    st.subheader("Pattern Analysis")
    st.json(analysis)
    
    # Generate API documentation
    if st.button("Generate API Documentation"):
        with st.spinner("Generating documentation..."):
            try:
                doc = analyzer.generate_api_documentation(results)
                st.text_area("Generated API Documentation", doc, height=400)
            except Exception as e:
                st.error(f"Documentation generation failed: {str(e)}")

def export_data():
    """Export the extracted data"""
    st.header("Export Data")
    
    if not hasattr(st.session_state, 'extraction_results'):
        st.info("No data to export. Please extract API details first.")
        return
    
    results = st.session_state.extraction_results
    
    # Export options
    export_format = st.selectbox("Export Format", ["JSON", "CSV", "YAML", "Markdown"])
    
    if st.button("Export Data"):
        try:
            if export_format == "JSON":
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(results, indent=2),
                    file_name="api_details.json",
                    mime="application/json"
                )
            elif export_format == "CSV":
                # Convert to CSV format
                csv_data = convert_to_csv(results)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="api_details.csv",
                    mime="text/csv"
                )
            # Add other formats as needed
            
        except Exception as e:
            st.error(f"Export failed: {str(e)}")

def convert_to_csv(results: dict) -> str:
    """Convert results to CSV format"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow(["Type", "URL", "Method", "Parameters", "Description"])
    
    # Write data
    for endpoint in results.get("endpoints", []):
        writer.writerow([
            "Endpoint",
            endpoint.get("url", ""),
            endpoint.get("method", ""),
            str(endpoint.get("parameters", "")),
            endpoint.get("description", "")
        ])
    
    return output.getvalue()

def show_settings(config: dict):
    """Show application settings"""
    st.header("Settings")
    
    st.subheader("GitHub Integration")
    github_token = st.text_input("GitHub Token", type="password", value=config.get("github_token", ""))
    
    st.subheader("Extraction Settings")
    max_depth = st.slider("Maximum Crawl Depth", 1, 10, config.get("max_depth", 3))
    timeout = st.number_input("Request Timeout (seconds)", 5, 60, config.get("timeout", 30))
    
    if st.button("Save Settings"):
        # Save settings logic here
        st.success("Settings saved!")

if __name__ == "__main__":
    main()
