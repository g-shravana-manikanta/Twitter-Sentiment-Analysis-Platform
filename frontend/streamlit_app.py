import os
import sys
import time
import requests
import streamlit as st
import html

# Configure Page Layout and Metadata
st.set_page_config(
    page_title="SentimentX - AI Capstone",
    page_icon="frontend/favicon.png",
    layout="wide"
)

# Backend API Configuration
BACKEND_URL = "https://twitter-sentiment-api-dcco.onrender.com"

# Initialize Session States
if "tweet_value" not in st.session_state:
    st.session_state.tweet_value = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "backend_status" not in st.session_state:
    st.session_state.backend_status = "Not Checked"

# Callback Helpers
def select_example(text):
    st.session_state.tweet_value = text

def clear_interface():
    st.session_state.tweet_value = ""
    if "last_prediction" in st.session_state:
        del st.session_state.last_prediction

# Check the health status of the FastAPI backend
def check_backend_health():
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=3.0)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                return "Online"
        return "Offline"
    except Exception:
        return "Offline"

# Query the API status on load
st.session_state.backend_status = check_backend_health()

# Custom Premium SentimentX Stylesheet (CSS)
st.markdown(
    """
    <style>
    /* Google Fonts Import */
    @import url("https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@800;900;700&f[]=satoshi@400;500;700;900&display=swap");
    @import url("https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap");
    
    /* Global Overrides */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: "Satoshi", -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #ffffff !important;
        color: #0f1419 !important;
    }
    
    /* Layout Max Width & Spacing Overrides */
    [data-testid="stMainBlockContainer"] {
        padding-top: 0px !important;
        padding-bottom: 2rem !important;
        max-width: 92% !important;
        margin: 0 auto !important;
    }
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        height: 0px !important;
        display: none !important;
    }
    .block-container {
        padding-top: 0px !important;
        padding-bottom: 2rem !important;
    }
    
    /* Background Grid Pattern */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: absolute;
        inset: 0;
        background-image:
            linear-gradient(to right, rgba(15, 20, 25, 0.035) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(15, 20, 25, 0.035) 1px, transparent 1px);
        background-size: 48px 48px;
        -webkit-mask-image: radial-gradient(ellipse 80% 60% at 50% 0%, #000 40%, transparent 100%);
        mask-image: radial-gradient(ellipse 80% 60% at 50% 0%, #000 40%, transparent 100%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Hide Default Streamlit Style Elements */
    #MainMenu {visibility: hidden;}
    footer[data-testid="stFooter"] {display: none !important;}
    div[data-testid="stDecoration"] {display: none;}
    
    /* Headers Typo settings */
    h1, h2, h3, h4, h5, h6 {
        font-family: "Cabinet Grotesk", "Satoshi", sans-serif !important;
        font-weight: 800 !important;
        color: #0f1419 !important;
    }
    
    .font-mono {
        font-family: "JetBrains Mono", monospace !important;
    }
    
    /* Premium Sticky Header styling for stHorizontalBlock */
    div[data-testid="stHorizontalBlock"]:first-child {
        border-bottom: 1px solid #EFF3F4;
        padding-bottom: 12px;
        margin-bottom: 25px;
        background-color: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }
    
    .header-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        text-decoration: none;
    }
    
    .header-title {
        font-family: "Cabinet Grotesk", sans-serif;
        font-size: 1.15rem;
        font-weight: 900;
        letter-spacing: -0.02em;
        color: #0F1419;
    }
    
    .nav-link {
        font-family: "JetBrains Mono", monospace;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        text-decoration: none;
        transition: color 0.2s ease;
        color: #536471;
    }
    
    .nav-link:hover {
        color: #1DA1F2 !important;
    }
    
    .header-status {
        display: flex;
        align-items: center;
        gap: 8px;
        border-radius: 9999px;
        border: 1px solid #EFF3F4;
        background-color: #ffffff;
        padding: 6px 12px;
        width: 100%;
        box-sizing: border-box;
    }
    
    .status-dot {
        position: relative;
        display: flex;
        height: 8px;
        width: 8px;
    }
    
    .status-ping {
        position: absolute;
        display: inline-flex;
        height: 100%;
        width: 100%;
        border-radius: 9999px;
        opacity: 0.6;
        animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;
    }
    
    .status-core {
        position: relative;
        display: inline-flex;
        border-radius: 9999px;
        height: 8px;
        width: 8px;
    }
    
    .status-text {
        font-family: "JetBrains Mono", monospace;
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #536471;
    }
    
    @keyframes ping {
        75%, 100% {
            transform: scale(2.5);
            opacity: 0;
        }
    }
    
    /* Hero Section styling */
    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 30px 0 10px 0;
        position: relative;
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        border-radius: 9999px;
        border: 1px solid #EFF3F4;
        background-color: #ffffff;
        padding: 6px 16px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    
    .hero-badge-text {
        font-family: "JetBrains Mono", monospace;
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #536471;
    }
    
    .hero-title {
        font-family: "Cabinet Grotesk", sans-serif;
        font-size: 4.2rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        line-height: 0.95;
        color: #0F1419;
        margin-bottom: 24px;
    }
    
    .hero-title-accent {
        color: #1DA1F2;
    }
    
    .hero-description {
        font-size: 1.12rem;
        line-height: 1.6;
        color: #536471;
        max-width: 650px;
        margin: 0 auto 36px auto;
    }
    
    .hero-description strong {
        color: #0F1419;
    }
    
    .hero-stats-strip {
        font-family: "JetBrains Mono", monospace;
        font-size: 0.72rem;
        font-weight: 700;
        color: #536471;
        background-color: #F7F9FA;
        padding: 10px 24px;
        border-radius: 9999px;
        border: 1px solid #EFF3F4;
        display: inline-flex;
        flex-wrap: wrap;
        gap: 16px;
        align-items: center;
        justify-content: center;
    }
    
    .hero-stats-strip span strong {
        color: #0F1419;
    }
    
    .stats-divider {
        color: #EFF3F4;
    }
    
    /* Interactive Card container wrappers */
    div[data-testid="column"] {
        position: relative !important;
    }
    
    /* Make markdown containers static so absolute background can align to the column boundaries */
    div[data-testid="column"] div[data-testid="element-container"],
    div[data-testid="column"] div[data-testid="stMarkdownContainer"] {
        position: static !important;
    }
    
    .input-card-bg {
        position: absolute;
        inset: -15px -15px -15px -15px;
        background-color: #ffffff;
        border: 1px solid #EFF3F4;
        border-radius: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        z-index: -1;
        pointer-events: none;
    }
    
    .card-heading {
        font-family: "Cabinet Grotesk", sans-serif;
        font-size: 1.25rem;
        font-weight: 800;
        color: #0F1419;
        margin-bottom: 4px;
    }
    
    .card-subheading {
        font-family: "JetBrains Mono", monospace;
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #8B98A5;
        margin-bottom: 20px;
        display: block;
    }
    
    /* Textarea overrides for premium card input field look */
    div[data-testid="stTextArea"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    div[data-testid="stTextArea"] textarea {
        background-color: #F7F9FA !important;
        color: #0F1419 !important;
        border: 1.5px solid #EFF3F4 !important;
        border-radius: 16px !important;
        font-size: 1.15rem !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
        padding: 16px !important;
        outline: none !important;
        box-shadow: none !important;
        min-height: 150px !important;
        font-family: "Satoshi", sans-serif !important;
        transition: all 0.25s ease !important;
    }
    div[data-testid="stTextArea"] textarea:focus {
        background-color: #ffffff !important;
        border-color: #1DA1F2 !important;
        box-shadow: 0 0 0 4px rgba(29, 161, 242, 0.1) !important;
        transform: translateY(-1px);
    }
    div[data-testid="stTextArea"] textarea::placeholder {
        color: #8B98A5 !important;
    }
    
    /* Live character counter overrides */
    .char-indicator-meta {
        font-family: "JetBrains Mono", monospace;
        font-size: 0.8rem;
        color: #8B98A5;
    }
    .char-counter-over {
        color: #D92D20 !important;
        font-weight: 700;
    }
    
    /* Buttons Custom Overrides */
    .stButton > button {
        border: 1px solid #EFF3F4 !important;
        background-color: #F7F9FA !important;
        color: #0F1419 !important;
        border-radius: 9999px !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        padding: 10px 20px !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: none !important;
    }
    .stButton > button:hover {
        border-color: #1DA1F2 !important;
        background-color: #F7F9FA !important;
        color: #1DA1F2 !important;
        transform: translateY(-1.5px);
    }
    
    /* Primary Action Buttons */
    button[kind="primary"] {
        background-color: #0F1419 !important;
        color: #ffffff !important;
        border-radius: 9999px !important;
        font-weight: 700 !important;
        padding: 12px 28px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(15, 20, 25, 0.12) !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    button[kind="primary"]:hover {
        background-color: #1DA1F2 !important;
        color: #ffffff !important;
        box-shadow: 0 6px 16px rgba(29, 161, 242, 0.3) !important;
        transform: translateY(-1.5px);
    }
    
    /* Awaiting Input Visual Container */
    .awaiting-input-card {
        background-color: #F7F9FA;
        border: 1.5px dashed #DCE3E7;
        border-radius: 24px;
        padding: 40px 30px;
        min-height: 360px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        transition: border-color 0.2s ease;
    }
    .awaiting-input-card:hover {
        border-color: #1DA1F2;
    }
    .awaiting-icon {
        color: #8B98A5;
        margin-bottom: 16px;
        animation: float 2.5s infinite ease-in-out;
    }
    .awaiting-title {
        font-family: "Cabinet Grotesk", sans-serif;
        font-size: 1.25rem;
        font-weight: 800;
        color: #0F1419;
        margin-bottom: 8px;
    }
    .awaiting-desc {
        font-size: 0.88rem;
        color: #8B98A5;
        max-width: 250px;
        line-height: 1.5;
        margin: 0 auto;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
        100% { transform: translateY(0px); }
    }
    
    /* Result Card Premium styling */
    .result-card {
        border-radius: 24px;
        padding: 32px;
        border: 1px solid;
        display: flex;
        flex-direction: column;
        position: relative;
        box-shadow: 0 4px 20px rgba(0,0,0,0.015);
    }
    
    .result-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    
    .result-card-header span {
        font-family: "JetBrains Mono", monospace;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }
    
    .result-card-body {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        margin-bottom: 24px;
    }
    
    .result-sentiment {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .result-emoji {
        font-size: 2.6rem;
        line-height: 1;
    }
    
    .result-verdict {
        font-family: "Satoshi", sans-serif;
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    
    .result-confidence {
        font-family: "Satoshi", sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        letter-spacing: -0.03em;
        line-height: 1.1;
        text-align: right;
    }
    
    .result-progress-container {
        width: 100%;
        border-radius: 9999px;
        height: 12px;
        overflow: hidden;
        margin-bottom: 24px;
    }
    
    .result-progress-fill {
        height: 100%;
        border-radius: 9999px;
        transition: width 1s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .result-card-footer {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        padding-top: 24px;
        border-top: 1px solid;
        font-family: "JetBrains Mono", monospace;
        font-size: 0.7rem;
    }
    
    /* Model Pipeline Section styling */
    .pipeline-section {
        margin-top: 100px;
        margin-bottom: 60px;
        width: 100%;
    }
    
    .pipeline-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        flex-wrap: wrap;
        gap: 20px;
        margin-bottom: 40px;
    }
    
    .pipeline-subtitle {
        font-family: "JetBrains Mono", monospace;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #1DA1F2;
        display: block;
        margin-bottom: 8px;
    }
    
    .pipeline-title {
        font-family: "Cabinet Grotesk", sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f1419;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .pipeline-desc-text {
        font-size: 0.95rem;
        line-height: 1.5;
        color: #536471;
        max-width: 380px;
        margin: 0;
    }
    
    .pipeline-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 30px;
    }
    
    @media (max-width: 768px) {
        .pipeline-grid {
            grid-template-columns: 1fr;
            gap: 24px;
        }
    }
    
    .pipeline-step-card {
        border-left: 2px solid #EFF3F4;
        padding-left: 24px;
        transition: border-color 0.25s ease;
    }
    
    .pipeline-step-card:hover {
        border-color: #1DA1F2;
    }
    
    .step-num {
        font-family: "JetBrains Mono", monospace;
        font-size: 0.88rem;
        font-weight: 700;
        color: #1DA1F2;
        margin-bottom: 12px;
    }
    
    .step-title {
        font-family: "Cabinet Grotesk", sans-serif;
        font-size: 1.25rem;
        font-weight: 800;
        color: #0f1419;
        margin: 0 0 8px 0;
    }
    
    .step-desc {
        font-size: 0.88rem;
        line-height: 1.5;
        color: #536471;
        margin: 0;
    }
    
    /* Recent Predictions Styling */
    .history-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        padding: 16px 20px;
        border: 1px solid #EFF3F4;
        background-color: #ffffff;
        border-radius: 16px;
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
        margin-bottom: 12px;
    }
    .history-item:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        border-color: #536471;
    }
    
    .history-text {
        font-size: 0.92rem;
        font-style: italic;
        color: #0f1419;
        font-weight: 500;
        max-width: 60%;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .history-meta {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    .history-timestamp {
        font-family: "JetBrains Mono", monospace;
        font-size: 0.72rem;
        color: #536471;
        text-align: right;
    }
    
    .history-badge {
        font-family: "JetBrains Mono", monospace;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 4px 12px;
        border-radius: 9999px;
    }
    
    /* Footer Area styling */
    .sentimentx-footer {
        border-top: 1px solid #EFF3F4;
        margin-top: 80px;
        padding: 40px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
        width: 100%;
    }
    
    .footer-logo-block {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .footer-logo-title {
        font-family: "Cabinet Grotesk", sans-serif;
        font-weight: 800;
        font-size: 1rem;
        color: #0F1419;
    }
    
    .footer-details {
        font-family: "JetBrains Mono", monospace;
        font-size: 0.7rem;
        color: #536471;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- HEADER COMPONENT ---
header_status_color = "#12B76A" if st.session_state.backend_status == "Online" else "#F04438"
header_status_text = "API Online" if st.session_state.backend_status == "Online" else "API Offline"

# Render the Header using columns
h_col1, h_col2 = st.columns([8.2, 3.8])

with h_col1:
    # Logo & Navigation Anchors
    st.markdown(
        """
        <div class="header-logo" style="margin-top: 10px;">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="#0F1419">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
            </svg>
            <span class="header-title">SentimentX</span>
            <span style="width: 25px;"></span>
            <a href="#analyzer" class="nav-link">Analyzer</a>
            <span style="width: 15px;"></span>
            <a href="#pipeline" class="nav-link">Pipeline</a>
            <span style="width: 15px;"></span>
            <a href="#history" class="nav-link">History</a>
        </div>
        """,
        unsafe_allow_html=True
    )

with h_col2:
    # Health status badge
    st.markdown(
        f"""
        <div class="header-status" style="margin-top: 2px;">
            <span class="status-dot">
                <span class="status-ping" style="background-color: {header_status_color};"></span>
                <span class="status-core" style="background-color: {header_status_color};"></span>
            </span>
            <span class="status-text">{header_status_text}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- HERO SECTION ---
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-badge">
            <span class="hero-badge-text">End-to-End AI Capstone</span>
        </div>
        <h1 class="hero-title">Decode the <span class="hero-title-accent">timeline.</span></h1>
        <p class="hero-description">
            A real-time tweet sentiment classifier. Type a post, hit predict, and read
            the polarity a Linear SVM extracted from <strong>1.6 million</strong> labelled tweets.
        </p>
        <div class="hero-stats-strip">
            <span>MODEL: <strong>SVM</strong></span>
            <span class="stats-divider">|</span>
            <span>TRAINED: <strong>1.6M TWEETS</strong></span>
            <span class="stats-divider">|</span>
            <span>ACCURACY: <strong>79.79%</strong></span>
            <span class="stats-divider">|</span>
            <span>HOST: <strong>FASTAPI BACKEND</strong></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Anchor element for navigation
st.markdown("<div id='analyzer' style='height: 40px;'></div>", unsafe_allow_html=True)

# Main Grid: Left Column (Text Input Layer) | Right Column (Classification Output)
layout_col1, layout_col2 = st.columns([6.7, 5.3], gap="large")

with layout_col1:
    # We place the absolute background card behind the column widgets
    st.markdown('<div class="input-card-bg"></div>', unsafe_allow_html=True)
    st.markdown('<span class="card-heading">Text Input Layer</span>', unsafe_allow_html=True)
    st.markdown('<span class="card-subheading">Select an example tweet</span>', unsafe_allow_html=True)
    
    # Example buttons row
    ex_col1, ex_col2, ex_col3, ex_col4 = st.columns([3.0, 3.2, 3.2, 2.6])
    with ex_col1:
        if st.button("😊 Love Phone", use_container_width=True):
            select_example("I absolutely love this new phone, the camera is amazing!")
            st.rerun()
    with ex_col2:
        if st.button("😊 Amazing Day", use_container_width=True):
            select_example("What an amazing day, everything went perfectly and I feel great!")
            st.rerun()
    with ex_col3:
        if st.button("😡 Terrible Service", use_container_width=True):
            select_example("The customer service was terrible and painfully slow.")
            st.rerun()
    with ex_col4:
        if st.button("😡 Worst Ever", use_container_width=True):
            select_example("its a worst and the design of the phone is not nice")
            st.rerun()
            
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # Native Streamlit Text Area styled to look borderless
    tweet_text = st.text_area(
        label="Input Area",
        max_chars=280,
        placeholder="Type a tweet to analyze its sentiment...",
        value=st.session_state.tweet_value,
        label_visibility="collapsed"
    )
    # Sync typed text to session state
    st.session_state.tweet_value = tweet_text
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    # Bottom actions row: Character Counter, Clear and Predict buttons side-by-side
    actions_col1, actions_col2, actions_col3 = st.columns([5.0, 2.8, 4.2])
    
    with actions_col1:
        char_len = len(tweet_text)
        if char_len > 280:
            st.markdown(f'<span class="char-indicator-meta char-counter-over" style="line-height: 42px;">Character Count: {char_len} / 280</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="char-indicator-meta" style="line-height: 42px;">Character Count: {char_len} / 280</span>', unsafe_allow_html=True)
            
    with actions_col2:
        # Styled Clear Button
        st.button("🧹 Clear", on_click=clear_interface, use_container_width=True)
        
    with actions_col3:
        # Styled Predict Button (Primary)
        predict_clicked = st.button("✨ Predict Sentiment", type="primary", use_container_width=True)
            
    # Call predict endpoint of FastAPI backend if button is clicked
    if predict_clicked:
        if not tweet_text.strip():
            st.error("⚠️ Input tweet cannot be empty. Please type or click an example.")
        else:
            # Check length limit before sending request
            if len(tweet_text) > 280:
                st.error("⚠️ Input length error: Tweet exceeds the maximum length of 280 characters.")
            else:
                with st.spinner("Calling API backend..."):
                    t_start = time.perf_counter()
                    try:
                        response = requests.post(
                            f"{BACKEND_URL}/predict",
                            json={"tweet": tweet_text},
                            timeout=10.0
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            prediction = data["prediction"]
                            confidence_score = data["confidence_score"]
                            t_duration = round((time.perf_counter() - t_start) * 1000)
                            t_stamp = time.strftime("%I:%M:%S %p")
                            
                            pred_record = {
                                "tweet": tweet_text,
                                "prediction": prediction,
                                "confidence_score": confidence_score,
                                "response_time_ms": t_duration,
                                "timestamp": t_stamp,
                                "raw_json": {
                                    "prediction": prediction,
                                    "confidence_score": confidence_score,
                                    "network_rtt_ms": t_duration
                                }
                            }
                            st.session_state.last_prediction = pred_record
                            
                            # Save to session history queue
                            st.session_state.history.insert(0, pred_record)
                            st.session_state.history = st.session_state.history[:5]
                            st.session_state.backend_status = "Online"
                            st.rerun()
                        elif response.status_code == 422:
                            st.error("⚠️ Input validation error: Tweet must be between 1 and 280 characters.")
                        else:
                            st.error(f"🚨 API Server returned status code {response.status_code}.")
                    except requests.exceptions.Timeout:
                        st.error("⏰ Connection timed out. The backend server on Render is waking up from its free tier sleep state. Please wait 1-2 minutes and try again.")
                    except Exception as e:
                        st.error(f"🚨 Failed to connect to API backend: {str(e)}")

# Right Column - Output cards and collapsible parameters
with layout_col2:
    st.markdown('<span class="card-heading">Classification Output</span>', unsafe_allow_html=True)
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    
    if "last_prediction" in st.session_state:
        pred = st.session_state.last_prediction
        pred_label = pred["prediction"]
        score = pred["confidence_score"]
        latency = pred["response_time_ms"]
        
        # Style variables mapping depending on prediction class
        if pred_label == "Positive":
            bg_color = "#E6F6EC"
            border_color = "#A6F4C5"
            text_color = "#039855"
            accent_color = "#12B76A"
            emoji = "😄"
            verdict = "POSITIVE"
        else:
            bg_color = "#FCE9E8"
            border_color = "#FECDCA"
            text_color = "#D92D20"
            accent_color = "#F04438"
            emoji = "😡"
            verdict = "NEGATIVE"
            
        request_metadata_json = {
            "text_length": len(pred["tweet"].split()),
            "vectorizer": "TfidfVectorizer",
            "classifier": "LinearSVC (API Engine)",
            "predicted_label": pred_label,
            "confidence": score,
            "latency_ms": latency,
            "raw_response": pred["raw_json"]
        }
        
        # Render custom HTML Result Card
        st.markdown(
            f"""
            <div class="result-card" style="background-color: {bg_color}; border-color: {border_color};">
                <div class="result-card-header">
                    <span style="color: {text_color};">Predicted Sentiment</span>
                    <span style="color: {text_color};">Confidence Score</span>
                </div>
                <div class="result-card-body">
                    <div class="result-sentiment">
                        <span class="result-emoji">{emoji}</span>
                        <span class="result-verdict" style="color: {text_color};">{verdict}</span>
                    </div>
                    <span class="result-confidence" style="color: {text_color};">{int(score * 100)}%</span>
                </div>
                <div class="result-progress-container" style="background-color: rgba(255,255,255,0.65);">
                    <div class="result-progress-fill" style="width: {int(score * 100)}%; background-color: {accent_color};"></div>
                </div>
                <div class="result-card-footer" style="border-color: {border_color}; color: {text_color};">
                    <div>Metric Type: <span style="font-weight: 700;">Estimated SVM Certainty</span></div>
                    <div style="text-align: right;">Inference Duration: <span style="font-weight: 700;">{latency} ms</span></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        # Request Details - Expandable Section
        with st.expander("🔍 View Request Metadata", expanded=False):
            st.json(request_metadata_json)
    else:
        # Styled Awaiting Input Visual Container
        st.markdown(
            """
            <div class="awaiting-input-card">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#8B98A5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="awaiting-icon">
                    <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
                    <path d="m5 3 1 2.5L8.5 6 6 7 5 9.5 4 7 1.5 6 4 5.5Z"/>
                    <path d="m19 17 1 2.5 2.5.5-2.5 1-1 2.5-1-2.5-2.5-1 2.5-1Z"/>
                </svg>
                <h3 class="awaiting-title">Awaiting Input</h3>
                <p class="awaiting-desc">Write or pick a tweet, then run the classifier to see its polarity here.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- THE PIPELINE MANIFESTO ---
st.markdown(
    """
    <section id="pipeline" class="pipeline-section">
      <div class="pipeline-header">
        <div>
          <span class="pipeline-subtitle">The Pipeline</span>
          <h2 class="pipeline-title">From raw text to polarity</h2>
        </div>
        <p class="pipeline-desc-text">
          Four deterministic stages turn 280 characters of opinion into a signed
          prediction and a certainty score.
        </p>
      </div>

      <div class="pipeline-grid">
        <div class="pipeline-step-card">
          <div class="step-num">01</div>
          <h3 class="step-title">Tokenize</h3>
          <p class="step-desc">The tweet is lowercased, stripped of noise and split into word tokens.</p>
        </div>
        <div class="pipeline-step-card">
          <div class="step-num">02</div>
          <h3 class="step-title">Vectorize</h3>
          <p class="step-desc">Tokens map to a sparse TF-IDF feature vector over the training vocabulary.</p>
        </div>
        <div class="pipeline-step-card">
          <div class="step-num">03</div>
          <h3 class="step-title">SVM Classify</h3>
          <p class="step-desc">A linear Support Vector Machine finds the side of the decision boundary.</p>
        </div>
        <div class="pipeline-step-card">
          <div class="step-num">04</div>
          <h3 class="step-title">Score</h3>
          <p class="step-desc">The distance from the hyperplane is squashed into a confidence percentage.</p>
        </div>
      </div>
    </section>
    """,
    unsafe_allow_html=True
)

# --- RECENT PREDICTIONS HISTORY QUEUE ---
st.markdown("<div id='history' style='height: 40px;'></div>", unsafe_allow_html=True)

hist_col1, hist_col2 = st.columns([9.0, 3.0])
with hist_col1:
    st.markdown(
        """
        <h2 class="pipeline-title" style="font-size: 1.7rem;">
            Recent Predictions <span style="color: #8B98A5; font-weight: 500; font-size: 1.25rem;">(Current Session)</span>
        </h2>
        """,
        unsafe_allow_html=True
    )
with hist_col2:
    if st.button("🗑️ Clear Prediction History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

if st.session_state.history:
    for item in st.session_state.history:
        label = item["prediction"]
        escaped_text = html.escape(item["tweet"])
        
        # Format tags matching React history cards
        if label == "Positive":
            bg_color = "#E6F6EC"
            border_color = "#A6F4C5"
            text_color = "#039855"
            emoji = "😄"
        else:
            bg_color = "#FCE9E8"
            border_color = "#FECDCA"
            text_color = "#D92D20"
            emoji = "😡"
            
        st.markdown(
            f"""
            <div class="history-item">
                <span class="history-text">"{escaped_text}"</span>
                <div class="history-meta">
                    <span class="history-timestamp">{item.get('timestamp', '')} &middot; Latency: {item['response_time_ms']} ms</span>
                    <span class="history-badge" style="background-color: {bg_color}; color: {text_color}; border: 1px solid {border_color};">
                        {emoji} {label.upper()} ({int(item['confidence_score'] * 100)}%)
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.markdown(
        "<p style='color: #8B98A5; font-style: italic; font-size: 0.9rem; padding: 20px 0;'>No predictions yet this session.</p>",
        unsafe_allow_html=True
    )

# --- FOOTER ---
st.markdown(
    """
    <div class="sentimentx-footer">
        <div class="footer-logo-block">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="#0F1419">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
            </svg>
            <span class="footer-logo-title">SentimentX</span>
        </div>
        <p class="footer-details">
            TF-IDF + Linear SVM &middot; Sentiment140 (1.6M tweets) &middot; Capstone
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
