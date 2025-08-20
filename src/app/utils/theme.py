"""
Beautiful theme utilities for Jeff's API Ripper
Provides modern, clean UI components with light backgrounds
"""

import streamlit as st

def apply_custom_page_config():
    """Apply custom page configuration with light theme"""
    st.set_page_config(
        page_title="Jeff's API Ripper",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply light theme with custom CSS
    apply_beautiful_theme()

def apply_beautiful_theme():
    """Apply beautiful light theme with subtle gradients"""
    st.markdown("""
        <style>
        /* Force light theme - override everything */
        .stApp {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        }
        
        .main {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        }
        
        .main .block-container {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Override any dark backgrounds */
        div[data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        }
        
        div[data-testid="stAppViewContainer"] > div {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        }
        
        /* Sidebar background - light gray */
        .css-1d391kg {
            background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%) !important;
        }
        
        /* Header styling */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            color: white;
            text-align: center;
        }
        
        .main-header h1 {
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        .main-header p {
            color: rgba(255,255,255,0.9);
            font-size: 1.2rem;
            margin: 0;
            opacity: 0.95;
        }
        
        /* Beautiful cards */
        .beautiful-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }
        
        .beautiful-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        }
        
        .beautiful-card h3 {
            color: #2d3748;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        
        .beautiful-card p {
            color: #4a5568;
            line-height: 1.6;
        }
        
        /* Beautiful dividers */
        .beautiful-divider {
            height: 2px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #667eea 100%);
            margin: 2rem 0;
            border-radius: 1px;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        /* Primary button */
        .stButton > button[data-baseweb="button"] {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
        }
        
        .stButton > button[data-baseweb="button"]:hover {
            box-shadow: 0 6px 20px rgba(72, 187, 120, 0.4);
        }
        
        /* Input fields */
        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 2px solid #e2e8f0;
            transition: all 0.3s ease;
            background: white !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* Select boxes */
        .stSelectbox > div > div {
            border-radius: 10px;
            border: 2px solid #e2e8f0;
            background: white !important;
        }
        
        /* File uploader */
        .stFileUploader > div {
            border-radius: 10px;
            border: 2px dashed #cbd5e0;
            background: #f7fafc !important;
        }
        
        /* Metrics */
        .metric-container {
            background: white;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
        }
        
        /* Expanders */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
            border-radius: 10px;
            border: 1px solid #e2e8f0;
            font-weight: 600;
            color: #2d3748;
        }
        
        /* Success/Error messages */
        .stAlert {
            border-radius: 10px;
            border: none;
        }
        
        /* Tabs */
        .stTabs > div > div > div > div {
            background: white;
            border-radius: 10px 10px 0 0;
            border: 1px solid #e2e8f0;
        }
        
        .stTabs > div > div > div > div[aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        /* Sidebar improvements */
        .css-1d391kg .css-1lcbmhc {
            background: white;
            border-radius: 10px;
            margin: 0.5rem;
            padding: 1rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        /* Force all text to be readable on light background */
        .main h1, .main h2, .main h3, .main p, .main div, .main span {
            color: #2d3748 !important;
        }
        
        /* Streamlit default elements */
        .stMarkdown, .stText, .stJson, .stCodeBlock {
            background: transparent !important;
            color: #2d3748 !important;
        }
        
        /* Remove any remaining dark elements */
        * {
            background-color: transparent !important;
        }
        
        .main .block-container, .main .block-container * {
            background: transparent !important;
        }
        
        /* Ensure proper contrast */
        .stMarkdown p, .stMarkdown div, .stMarkdown span {
            color: #2d3748 !important;
        }
        
        /* Force light theme on all elements */
        div[class*="st"], div[class*="css"] {
            background: transparent !important;
        }
        
        /* Override any Streamlit dark theme */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        }
        
        [data-testid="stAppViewContainer"] * {
            background: transparent !important;
        }
        
        </style>
        """, unsafe_allow_html=True)

def create_beautiful_header(title: str, subtitle: str, icon: str):
    """Create a beautiful header with gradient background"""
    st.markdown(f"""
        <div class="main-header">
            <h1>{icon} {title}</h1>
            <p>{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)

def create_beautiful_card(content: str, title: str, icon: str):
    """Create a beautiful card with light background"""
    st.markdown(f"""
        <div class="beautiful-card">
            <h3>{icon} {title}</h3>
            {content}
        </div>
        """, unsafe_allow_html=True)

def create_beautiful_divider():
    """Create a beautiful gradient divider"""
    st.markdown('<div class="beautiful-divider"></div>', unsafe_allow_html=True)

def create_metric_card(label: str, value: str, icon: str = ""):
    """Create a beautiful metric card"""
    st.markdown(f"""
        <div class="metric-container">
            <h4>{icon} {label}</h4>
            <p style="font-size: 1.5rem; font-weight: 700; color: #667eea; margin: 0;">{value}</p>
        </div>
        """, unsafe_allow_html=True)
