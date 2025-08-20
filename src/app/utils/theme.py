"""
Beautiful theme configuration for Jeff's API Ripper
"""

import streamlit as st
from typing import Dict, Any

def apply_beautiful_theme():
    """Apply a beautiful, modern theme to the Streamlit app"""
    
    # Custom CSS for beautiful styling
    st.markdown("""
    <style>
    /* Main theme colors and fonts */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Beautiful headers */
    h1, h2, h3 {
        color: #2c3e50 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        font-weight: 600 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    
    h2 {
        font-size: 2rem !important;
        color: #34495e !important;
        border-bottom: 3px solid #3498db !important;
        padding-bottom: 0.5rem !important;
    }
    
    h3 {
        font-size: 1.5rem !important;
        color: #2c3e50 !important;
        border-left: 4px solid #3498db !important;
        padding-left: 1rem !important;
    }
    
    /* Beautiful buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Primary button styling */
    .stButton > button[data-baseweb="button"] {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%) !important;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.4) !important;
    }
    
    .stButton > button[data-baseweb="button"]:hover {
        box-shadow: 0 6px 20px rgba(52, 152, 219, 0.6) !important;
    }
    
    /* Beautiful text inputs */
    .stTextInput > div > div > input {
        border: 2px solid #e0e6ed !important;
        border-radius: 15px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        background: white !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3498db !important;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Beautiful selectboxes */
    .stSelectbox > div > div > div {
        border: 2px solid #e0e6ed !important;
        border-radius: 15px !important;
        background: white !important;
    }
    
    .stSelectbox > div > div > div:hover {
        border-color: #3498db !important;
    }
    
    /* Beautiful file uploader */
    .stFileUploader > div > div {
        border: 2px dashed #3498db !important;
        border-radius: 15px !important;
        background: rgba(52, 152, 219, 0.05) !important;
        padding: 2rem !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #2980b9 !important;
        background: rgba(52, 152, 219, 0.1) !important;
        transform: scale(1.02) !important;
    }
    
    /* Beautiful sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%) !important;
        color: white !important;
    }
    
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: white !important;
        text-shadow: none !important;
    }
    
    /* Beautiful tabs */
    .stTabs > div > div > div > div {
        background: white !important;
        border-radius: 15px 15px 0 0 !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
    }
    
    .stTabs > div > div > div > div > button {
        border-radius: 15px 15px 0 0 !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs > div > div > div > div > button[aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* Beautiful expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #ecf0f1 0%, #bdc3c7 100%) !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
        color: #2c3e50 !important;
    }
    
    .streamlit-expanderContent {
        background: white !important;
        border-radius: 0 0 10px 10px !important;
        border: 1px solid #e0e6ed !important;
        margin-top: 0 !important;
    }
    
    /* Beautiful success/error messages */
    .stAlert {
        border-radius: 15px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }
    
    /* Beautiful dataframes */
    .stDataFrame {
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }
    
    /* Beautiful JSON displays */
    .stJson {
        background: #f8f9fa !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        border: 1px solid #e0e6ed !important;
    }
    
    /* Beautiful code blocks */
    .stCodeBlock {
        background: #2c3e50 !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }
    
    /* Beautiful progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 10px !important;
    }
    
    /* Beautiful spinners */
    .stSpinner > div {
        border: 3px solid #f3f3f3 !important;
        border-top: 3px solid #3498db !important;
        border-radius: 50% !important;
    }
    
    /* Custom card styling */
    .custom-card {
        background: white !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1) !important;
        border: 1px solid #e0e6ed !important;
        transition: all 0.3s ease !important;
    }
    
    .custom-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 12px 35px rgba(0,0,0,0.15) !important;
    }
    
    /* Beautiful dividers */
    .divider {
        height: 3px !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 2px !important;
        margin: 2rem 0 !important;
    }
    
    /* Beautiful icons */
    .icon-large {
        font-size: 3rem !important;
        margin: 1rem 0 !important;
        text-align: center !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        h1 { font-size: 2rem !important; }
        h2 { font-size: 1.5rem !important; }
        h3 { font-size: 1.25rem !important; }
        
        .custom-card {
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
        }
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%) !important;
        }
        
        .custom-card {
            background: #2d2d2d !important;
            color: white !important;
            border-color: #404040 !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_beautiful_header(title: str, subtitle: str = "", icon: str = "🔍"):
    """Create a beautiful header with gradient text and icon"""
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <div class="icon-large">{icon}</div>
        <h1>{title}</h1>
        {f'<p style="font-size: 1.2rem; color: #7f8c8d; margin-top: 1rem;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def create_beautiful_card(content: str, title: str = "", icon: str = ""):
    """Create a beautiful card with content"""
    icon_html = f'<div style="font-size: 2rem; margin-bottom: 1rem;">{icon}</div>' if icon else ""
    title_html = f'<h3 style="margin-bottom: 1rem;">{title}</h3>' if title else ""
    
    st.markdown(f"""
    <div class="custom-card">
        {icon_html}
        {title_html}
        {content}
    </div>
    """, unsafe_allow_html=True)

def create_beautiful_divider():
    """Create a beautiful gradient divider"""
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

def apply_custom_page_config():
    """Apply custom page configuration with beautiful theme"""
    st.set_page_config(
        page_title="Jeff's API Ripper",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply the beautiful theme
    apply_beautiful_theme()
    
    # Hide default Streamlit elements
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)
