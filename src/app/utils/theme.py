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
    """Apply beautiful light theme with subtle blue gradients"""
    st.markdown("""
        <style>
        /* Force light theme - override everything */
        .stApp {
            background: linear-gradient(135deg, #f8faff 0%, #f0f4ff 100%) !important;
        }
        
        .main {
            background: linear-gradient(135deg, #f8faff 0%, #f0f4ff 100%) !important;
        }
        
        .main .block-container {
            background: linear-gradient(135deg, #f8faff 0%, #f0f4ff 100%) !important;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Override any dark backgrounds */
        div[data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #f8faff 0%, #f0f4ff 100%) !important;
        }
        
        div[data-testid="stAppViewContainer"] > div {
            background: linear-gradient(135deg, #f8faff 0%, #f0f4ff 100%) !important;
        }
        
        /* Sidebar background - very light blue */
        .css-1d391kg {
            background: linear-gradient(180deg, #fafbff 0%, #f5f7ff 100%) !important;
        }
        
        /* Header styling */
        .main-header {
            background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
            padding: 2.5rem;
            border-radius: 20px;
            margin-bottom: 2.5rem;
            box-shadow: 0 15px 35px rgba(79, 70, 229, 0.2);
            color: white;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.1) 100%);
            pointer-events: none;
        }
        
        .main-header h1 {
            color: white;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.75rem;
            text-shadow: 0 3px 6px rgba(0,0,0,0.3);
            letter-spacing: -0.02em;
        }
        
        .main-header p {
            color: rgba(255,255,255,0.95);
            font-size: 1.3rem;
            margin: 0;
            opacity: 0.95;
            font-weight: 400;
        }
        
        /* Beautiful cards */
        .beautiful-card {
            background: linear-gradient(135deg, #ffffff 0%, #fafbff 100%);
            border-radius: 20px;
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: 0 8px 25px rgba(79, 70, 229, 0.08);
            border: 1px solid #e0e7ff;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .beautiful-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
        }
        
        .beautiful-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 40px rgba(79, 70, 229, 0.15);
        }
        
        .beautiful-card h3 {
            color: #3730a3;
            margin-bottom: 1.5rem;
            font-weight: 700;
            font-size: 1.4rem;
            letter-spacing: -0.01em;
        }
        
        .beautiful-card p {
            color: #374151;
            line-height: 1.7;
            font-size: 1.05rem;
        }
        
        /* Beautiful dividers */
        .beautiful-divider {
            height: 3px;
            background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 50%, #4f46e5 100%);
            margin: 3rem 0;
            border-radius: 2px;
            position: relative;
        }
        
        .beautiful-divider::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 20px;
            height: 20px;
            background: #4f46e5;
            border-radius: 50%;
            box-shadow: 0 0 0 4px #f8faff;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 6px 20px rgba(79, 70, 229, 0.25);
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .stButton > button:hover::before {
            left: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(79, 70, 229, 0.35);
        }
        
        /* Primary button */
        .stButton > button[data-baseweb="button"] {
            background: linear-gradient(135deg, #059669 0%, #047857 100%);
            box-shadow: 0 6px 20px rgba(5, 150, 105, 0.25);
        }
        
        .stButton > button[data-baseweb="button"]:hover {
            box-shadow: 0 10px 30px rgba(5, 150, 105, 0.35);
        }
        
        /* Input fields */
        .stTextInput > div > div > input {
            border-radius: 12px;
            border: 2px solid #c7d2fe;
            transition: all 0.3s ease;
            background: white !important;
            padding: 0.75rem 1rem;
            font-size: 1rem;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #4f46e5;
            box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
            transform: translateY(-1px);
        }
        
        /* Select boxes */
        .stSelectbox > div > div {
            border-radius: 12px;
            border: 2px solid #c7d2fe;
            background: white !important;
        }
        
        /* File uploader */
        .stFileUploader > div {
            border-radius: 12px;
            border: 2px dashed #a5b4fc;
            background: #f8faff !important;
            padding: 2rem;
        }
        
        /* Metrics */
        .metric-container {
            background: linear-gradient(135deg, #ffffff 0%, #fafbff 100%);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 0.75rem;
            box-shadow: 0 4px 20px rgba(79, 70, 229, 0.08);
            border: 1px solid #e0e7ff;
            text-align: center;
        }
        
        /* Expanders */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #f8faff 0%, #f0f4ff 100%);
            border-radius: 12px;
            border: 1px solid #c7d2fe;
            font-weight: 600;
            color: #3730a3;
            padding: 1rem 1.5rem;
        }
        
        /* Success/Error messages */
        .stAlert {
            border-radius: 12px;
            border: none;
        }
        
        /* Tabs */
        .stTabs > div > div > div > div {
            background: white;
            border-radius: 12px 12px 0 0;
            border: 1px solid #c7d2fe;
            font-weight: 600;
        }
        
        .stTabs > div > div > div > div[aria-selected="true"] {
            background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
            color: white;
        }
        
        /* Sidebar improvements */
        .css-1d391kg .css-1lcbmhc {
            background: linear-gradient(135deg, #ffffff 0%, #fafbff 100%);
            border-radius: 16px;
            margin: 0.75rem;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(79, 70, 229, 0.08);
            border: 1px solid #e0e7ff;
        }
        
        /* Force all text to be readable on light background */
        .main h1, .main h2, .main h3, .main p, .main div, .main span {
            color: #1f2937 !important;
        }
        
        /* Streamlit default elements */
        .stMarkdown, .stText, .stJson, .stCodeBlock {
            background: transparent !important;
            color: #1f2937 !important;
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
            color: #1f2937 !important;
        }
        
        /* Force light theme on all elements */
        div[class*="st"], div[class*="css"] {
            background: transparent !important;
        }
        
        /* Override any Streamlit dark theme */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #f8faff 0%, #f0f4ff 100%) !important;
        }
        
        [data-testid="stAppViewContainer"] * {
            background: transparent !important;
        }
        
        /* Additional blue accents */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #3730a3 !important;
        }
        
        /* Sidebar headers */
        .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
            color: #3730a3 !important;
        }
        
        /* Info boxes */
        .stAlert[data-baseweb="notification"] {
            background: linear-gradient(135deg, #f8faff 0%, #f0f4ff 100%) !important;
            border: 1px solid #a5b4fc !important;
            color: #3730a3 !important;
            border-radius: 12px;
        }
        
        /* Success messages */
        .stAlert[data-baseweb="notification"][data-status="success"] {
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%) !important;
            border: 1px solid #86efac !important;
            color: #166534 !important;
            border-radius: 12px;
        }
        
        /* Warning messages */
        .stAlert[data-baseweb="notification"][data-status="warning"] {
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%) !important;
            border: 1px solid #fbbf24 !important;
            color: #92400e !important;
            border-radius: 12px;
        }
        
        /* Error messages */
        .stAlert[data-baseweb="notification"][data-status="error"] {
            background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%) !important;
            border: 1px solid #fca5a5 !important;
            color: #991b1b !important;
            border-radius: 12px;
        }
        
        /* Rich styling for headers */
        .stMarkdown h1 {
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #3730a3 0%, #4f46e5 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
            margin-bottom: 1.5rem !important;
        }
        
        .stMarkdown h2 {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: #4f46e5 !important;
            border-bottom: 3px solid #e0e7ff !important;
            padding-bottom: 0.5rem !important;
            margin-bottom: 1.5rem !important;
        }
        
        .stMarkdown h3 {
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            color: #3730a3 !important;
            margin-bottom: 1rem !important;
        }
        
        /* Enhanced sidebar styling */
        .css-1d391kg {
            border-right: 2px solid #e0e7ff !important;
        }
        
        /* Rich card hover effects */
        .beautiful-card:hover::before {
            background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 50%, #4f46e5 100%);
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
