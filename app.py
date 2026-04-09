import streamlit as st
import time
import google.generativeai as genai
import tempfile
import os
import random
from PIL import Image

# --- 1. API CONFIGURATION (REQUIRED) ---
# Paste your real Google AI Studio key inside the quotes
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"

# --- 2. Page Configuration ---
st.set_page_config(
    page_title="Agent Ecosystem • AI Workspace",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# --- 3. Ultra-Premium "MAANG" CSS Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Animated Dark Breathing Background */
    .stApp {
        background: linear-gradient(-45deg, #0b0b0f, #161622, #0f0f16, #0b0b0f);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #EDEDED;
        font-family: 'Inter', sans-serif !important;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    #MainMenu, footer, header {visibility: hidden;}

    /* Reduced padding-top to pull everything up and prevent scrolling */
    .block-container {
        padding-top: 1.5rem !important; 
        padding-bottom: 0rem !important;
        max-width: 1200px !important;
    }

    h1, h2, h3 { color: #FFFFFF !important; font-weight: 600 !important; letter-spacing: -0.02em !important; }

    /* Custom Webkit Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.3); }

    /* Enhanced Glassmorphism Form Containers */
    [data-testid="stForm"] {
        background: rgba(20, 20, 25, 0.4) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        padding: 40px 45px !important;
        margin-top: 15px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    }

    /* --- PREMIUM SLEEK INPUT FIELDS --- */
    .stTextInput div[data-baseweb="input"], .stTextArea div[data-baseweb="textarea"] {
        background-color: rgba(15, 15, 20, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        outline: none !important;
        box-shadow: none !important;
    }
    
    .stTextInput div[data-baseweb="input"]:focus-within, .stTextArea div[data-baseweb="textarea"]:focus-within {
        border-color: #00e5ff !important;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.25) !important;
        background-color: rgba(25, 25, 35, 0.8) !important;
    }

    .stTextInput input, .stTextArea textarea {
        background-color: transparent !important;
        border: none !important;
        color: #FFFFFF !important;
        padding: 14px 18px !important;
        font-size: 1rem !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        background-color: transparent !important;
    }
    
    div[data-baseweb="base-input"] {
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }
    
    [data-testid="InputInstructions"] { display: none !important; }

    /* --- PREMIUM BUTTON STYLING --- */
    button[kind="primary"] {
        background: linear-gradient(135deg, #00e5ff 0%, #0077ff 100%) !important;
        color: #FFFFFF !important;  
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        border-radius: 50px !important;
        padding: 14px 30px !important;
        border: none !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-size: 1.05rem !important;
        box-shadow: 0 8px 25px -5px rgba(0, 229, 255, 0.5) !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 35px -5px rgba(0, 229, 255, 0.6) !important;
        background: linear-gradient(135deg, #33eeff 0%, #0099ff 100%) !important;
    }

    /* Secondary Buttons */
    button[kind="secondary"], button[kind="secondaryFormSubmit"] {
        background: rgba(30, 30, 35, 0.5) !important;
        backdrop-filter: blur(12px) !important;
        color: #EDEDED !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        transition: all 0.3s ease !important;
    }
    
    button[kind="secondary"]:hover, button[kind="secondary"]:focus,
    button[kind="secondaryFormSubmit"]:hover, button[kind="secondaryFormSubmit"]:focus {
        border-color: #00e5ff !important;
        color: #00e5ff !important;
        background: rgba(0, 229, 255, 0.08) !important;
        box-shadow: 0 4px 20px rgba(0, 229, 255, 0.2) !important;
    }
    
    button[kind="secondary"]:active, button[kind="secondaryFormSubmit"]:active {
        border-color: #00e5ff !important;
        color: #00e5ff !important;
        background: rgba(0, 229, 255, 0.2) !important;
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.5) !important;
        transform: scale(0.98);
    }

    /* --- NATIVE DROPDOWN (SELECTBOX) STYLING WITH DISABLED SEARCH FEEL --- */
    div[data-baseweb="select"] > div {
        background: rgba(35, 35, 45, 0.5) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        height: 46px !important;
        cursor: pointer !important;
        color: #EDEDED !important;
    }
    div[data-baseweb="select"]:hover > div {
        border-color: rgba(0, 229, 255, 0.5) !important;
    }
    /* HIDE TYPING CURSOR TO DISABLE "EDIT" FEEL */
    div[data-baseweb="select"] input {
        caret-color: transparent !important; 
        cursor: pointer !important;
    }
    /* Dropdown list container matching theme */
    div[data-baseweb="popover"] ul {
        background: rgba(25, 25, 30, 0.98) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
    }
    /* Dropdown items */
    li[role="option"] {
        color: #EDEDED !important;
        background: transparent !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    li[role="option"]:hover, li[role="option"][aria-selected="true"] {
        background-color: rgba(0, 229, 255, 0.15) !important;
        color: #00e5ff !important;
    }

    /* --- SMALL BUTTONS FOR IN-PLACE EDIT MODE --- */
    .small-btn div[data-testid="stButton"] button {
        padding: 4px 12px !important;
        font-size: 0.85rem !important;
        height: 32px !important;
        min-height: 32px !important;
        border-radius: 8px !important;
        width: 100% !important;
    }

    /* --- NEW SIMPLE HISTORY LIST BUTTONS --- */
    .history-link-btn div[data-testid="stButton"] button {
        background-color: transparent !important;
        color: #EDEDED !important;
        border: none !important;
        box-shadow: none !important;
        padding: 12px 10px !important;
        margin: 0 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    .history-link-btn div[data-testid="stButton"] button:hover {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #00e5ff !important;
        transform: translateX(5px) !important;
    }

    /* --- CHAT ELEMENTS & AVATARS --- */
    .stChatMessage { 
        background-color: transparent !important; 
        border: none !important; 
        padding: 1.5rem 0 !important;
        animation: slideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    [data-testid="chat-message-user"] div[data-testid="stChatMessageAvatarUser"] {
        background: linear-gradient(135deg, #00e5ff 0%, #2196F3 100%) !important;
        color: #000000 !important;
        box-shadow: 0 4px 12px rgba(0, 229, 255, 0.3);
    }
    
    [data-testid="chat-message-assistant"] div[data-testid="stChatMessageAvatarAssistant"] {
        background-color: #121218 !important;
        border: 1px solid #00e5ff !important;
        color: #00e5ff !important;
    }
    
    [data-testid="chat-message-assistant"] { 
        background: rgba(25, 25, 32, 0.4) !important; 
        backdrop-filter: blur(12px) !important;
        border-radius: 18px; 
        border: 1px solid rgba(255, 255, 255, 0.05); 
        padding: 1.5rem !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }

    /* --- GLOWING GLASSMORPHISM PROMPT BLOCK (Fixing Red & Double Borders) --- */
    [data-testid="stChatInput"] { 
        background-color: transparent !important; 
        border: none !important; 
        box-shadow: none !important;
        outline: none !important;
        padding-bottom: 25px !important; 
    }
    
    /* Target the exact wrapper Streamlit uses for the outline */
    [data-testid="stChatInput"] > div {
        background: rgba(25, 25, 32, 0.65) !important; 
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(0, 229, 255, 0.3) !important; 
        border-radius: 35px !important; 
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    /* Pure blue focus for the entire container, suppressing default red */
    [data-testid="stChatInput"] > div:focus-within {
        border: 1px solid #00e5ff !important; 
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.3) !important; 
        background: rgba(30, 30, 40, 0.85) !important;
        outline: none !important;
    }
    
    /* Ensure inner textarea doesn't generate a second border */
    [data-testid="stChatInput"] textarea {
        background: transparent !important; 
        border: none !important;
        color: white !important; 
        padding: 18px 28px !important; 
        font-size: 1.05rem !important; 
        min-height: 65px !important; 
        box-shadow: none !important;
        outline: none !important;
    }
    
    [data-testid="stChatInput"] textarea:focus { 
        border: none !important; 
        box-shadow: none !important; 
        outline: none !important; 
    }
    
    /* --- EDITING MODE STYLING --- */
    .edit-mode-container {
        background: rgba(25, 25, 32, 0.8) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(0, 229, 255, 0.4) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 0 10px 40px rgba(0, 229, 255, 0.15) !important;
        margin-bottom: 20px;
        animation: slideUp 0.3s ease;
    }

    /* --- INLINE CHAT ACTION ICONS --- */
    .action-icons div[data-testid="stButton"] button {
        background-color: transparent !important; 
        color: #2196F3 !important; 
        border: none !important; 
        box-shadow: none !important; 
        padding: 0 !important; 
        margin: 0 !important; 
        width: 34px !important; 
        height: 34px !important;
        min-height: 34px !important;
        font-size: 1.15rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 10px !important; 
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .action-icons div[data-testid="stButton"] button:hover { 
        color: #64B5F6 !important; 
        background-color: rgba(33, 150, 243, 0.15) !important; 
        transform: scale(1.1); 
    }
    .action-icons div[data-testid="stButton"] button:active {
        transform: scale(0.95);
    }

    /* --- ATTACHMENT POPOVER BUTTONS --- */
    div[data-testid="stPopover"] > button {
        width: 100% !important;
        height: 46px !important;
        display: flex; justify-content: center; align-items: center;
        background: rgba(35, 35, 45, 0.5) !important;
        backdrop-filter: blur(12px) !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
    }
    div[data-testid="stPopoverBody"] div[data-testid="stButton"] button {
        text-align: left !important; width: 100% !important; border: none !important; background: transparent !important;
        color: #EDEDED !important; padding: 12px 18px !important; border-radius: 10px !important; font-weight: 500 !important; transition: all 0.2s ease;
    }
    div[data-testid="stPopoverBody"] div[data-testid="stButton"] button:hover { 
        background-color: rgba(0, 229, 255, 0.12) !important; 
        color: #00e5ff !important; 
        padding-left: 24px !important; 
    }
    
    /* --- HEADER BUTTONS SIZING --- */
    .header-btn div[data-testid="stButton"] button {
        width: 100% !important;
        height: 46px !important;       
        min-height: 46px !important;   
        padding: 0 20px !important;    
        margin-top: 0px !important;
        white-space: nowrap !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-weight: 500 !important;
    }
    
    /* Gradient Text for Main Logo & Headings */
    .gradient-text {
        background: linear-gradient(135deg, #FFFFFF 0%, #00e5ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. State Management ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'selected_agent' not in st.session_state: st.session_state.selected_agent = "Research Agent"
if 'messages' not in st.session_state: st.session_state.messages = []
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'selected_model' not in st.session_state: st.session_state.selected_model = "Fast (Answers quickly)"

# Edit States
if 'edit_message_index' not in st.session_state: st.session_state.edit_message_index = None
if 'edit_input_value' not in st.session_state: st.session_state.edit_input_value = ""
if 'pending_edit_generation' not in st.session_state: st.session_state.pending_edit_generation = False

# Dynamic History State
if 'history_view' not in st.session_state: st.session_state.history_view = False
if 'history_data' not in st.session_state: st.session_state.history_data = []

# --- 5. HIGH-SPEED REAL INTELLIGENCE BACKEND WITH Caching & Auto-Closing ---

# CACHE THE AUTO-DISCOVERY TO ELIMINATE ALL LAG (Checks Google servers only once)
@st.cache_data(show_spinner=False, ttl=3600)
def get_optimal_model(api_key):
    try:
        genai.configure(api_key=api_key)
        available_models = [m.name.replace('models/', '') for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        preferred_models = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro', 'gemini-pro']
        for pref in preferred_models:
            if pref in available_models:
                return pref
        return available_models[0] if available_models else 'gemini-1.5-flash'
    except Exception:
        # Failsafe if network is blocked during initial discovery
        return 'gemini-1.5-flash'

def run_agent_stream(agent_name, prompt, model_tier, files=None):
    """Yields text chunks instantly. Automatically retries if you click too fast."""
    if not GOOGLE_API_KEY or GOOGLE_API_KEY.strip() == "" or GOOGLE_API_KEY == "YOUR_API_KEY_HERE":
        time.sleep(0.5)
        yield "⚠️ **API Key Required:**\n\nIt looks like you haven't added your API key yet. Please paste your valid key into line 11 of the code."
        return
    
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Grab the ultra-fast, perfectly supported model for this specific computer
    target_model_name = get_optimal_model(GOOGLE_API_KEY)
    model = genai.GenerativeModel(target_model_name) 
    
    # --- AGENT PERSONAS ---
    agent_personas = {
        "Research Agent": "You are an expert research analyst. Provide factual, detailed, and highly accurate information.",
        "Writing Agent": "You are a senior copywriter and editor. Your task is to write engaging, creative, and well-structured content.",
        "Code Agent": "You are a senior software engineer. Provide clean, highly efficient, and bug-free code. Always include comments.",
        "Review Agent": "You are a strict QA reviewer. Critique the user's prompt or text. Point out logical flaws, mistakes, and suggest improvements.",
        "Deep Research": "You are a Deep Research AI. Conduct comprehensive, multi-step analysis on the user's prompt. Provide extensive, deeply researched information.",
        "Guided Learning": "You are an expert, empathetic tutor. Break down complex topics step-by-step. Use clear analogies and ensure foundational understanding."
    }
    
    system_instruction = agent_personas.get(agent_name, "You are a helpful AI assistant.")
    if "Thinking" in model_tier:
        system_instruction += " Before giving your final answer, you MUST think step-by-step and show your reasoning process."
    elif "Pro" in model_tier:
        system_instruction += " Provide a highly advanced, expert-level response. Ensure all logic and code is production-ready."
    
    full_prompt = f"System Instructions for you: {system_instruction}\n\nUser Prompt: {prompt}"
    
    content_payload = [full_prompt]
    
    if files:
        for f in files:
            if f.type in ['text/plain', 'text/csv']:
                file_text = f.getvalue().decode('utf-8')
                content_payload.append(f"\n[Attached Document: {f.name}]\n{file_text}")
            elif f.type == 'application/pdf':
                yield "⚠️ Note: For this presentation demo, please copy-paste the text directly from the PDF instead of uploading it.\n\n"
            elif f.type.startswith('image/'):
                yield "⚠️ Note: For this presentation demo, please describe the image in text rather than uploading it.\n\n"

    # --- AUTOMATIC RETRY LOGIC FOR QUOTA 429 ERRORS ---
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content(content_payload, stream=True)
            for chunk in response:
                yield chunk.text
            return 
            
        except Exception as inner_e:
            error_msg = str(inner_e).lower()
            
            if "429" in error_msg or "quota" in error_msg or "exhausted" in error_msg:
                if attempt < max_retries - 1:
                    time.sleep(3) 
                    continue
                else:
                    yield "\n\n⚠️ **Rate Limit Exceeded:** You are sending requests too quickly for the free tier. Please wait about 30 seconds before sending the next message."
                    return
            elif "api_key" in error_msg or "400" in error_msg or "403" in error_msg or "unauthenticated" in error_msg:
                yield "⚠️ **Authentication Error:** The API Key provided on Line 11 is invalid or missing permissions."
                return
            else:
                yield f"⚠️ **System Error:** {str(inner_e)}\n\nPlease check your internet connection."
                return

# --- 6. Page Definitions ---

def welcome_page():
    st.markdown("<h1 style='text-align: center; font-size: 5rem; margin-bottom: 0;'><span class='gradient-text'>Multi Agent Chatbot</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A0A0AB; font-size: 1.2rem; margin-top: 15px; margin-bottom: 35px; max-width: 800px; margin-left: auto; margin-right: auto; line-height: 1.6;'>A collaborative ecosystem of specialized AI agents designed to seamlessly execute complex workflows, automate research, and drive intelligent decision-making.</p>", unsafe_allow_html=True)
    _, col_center, _ = st.columns([1, 1.2, 1])
    with col_center:
        with st.form("welcome_form"):
            st.markdown("<p style='font-size: 0.95rem; font-weight: 500; margin-bottom: 8px; color: #EDEDED;'>Enter your name to begin</p>", unsafe_allow_html=True)
            name_input = st.text_input("Name", value=st.session_state.user_name, label_visibility="collapsed", placeholder="Your name...")
            
            if st.form_submit_button("Proceed to Login", use_container_width=True):
                if name_input.strip():
                    st.session_state.user_name = name_input.strip()
                    st.session_state.page = 'login'; st.rerun()
                else: st.error("Please enter a name.")

def login_page():
    st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-bottom: 0;'><span class='gradient-text'>System Login</span></h1>", unsafe_allow_html=True)
    greeting = f"Welcome, <span style='color: #00e5ff; font-weight: 600;'>{st.session_state.user_name}</span>!" if st.session_state.user_name else "Authenticate to access the agent ecosystem."
    st.markdown(f"<p style='text-align: center; color: #A0A0AB; font-size: 1.2rem; margin-top: 10px; margin-bottom: 30px;'>{greeting}</p>", unsafe_allow_html=True)
    _, col_center, _ = st.columns([1, 1.2, 1])
    with col_center:
        with st.form("login_form"):
            st.markdown("<p style='font-size: 0.95rem; font-weight: 500; margin-bottom: 8px; color: #EDEDED;'>Username</p>", unsafe_allow_html=True)
            username_input = st.text_input("Username", value=st.session_state.user_name, label_visibility="collapsed", placeholder="Enter your username...")
            st.markdown("<p style='font-size: 0.95rem; font-weight: 500; margin-top: 20px; margin-bottom: 8px; color: #EDEDED;'>Password</p>", unsafe_allow_html=True)
            password_input = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="••••••••")
            
            if st.form_submit_button("Authenticate", use_container_width=True):
                if username_input.strip() and password_input.strip():
                    st.session_state.user_name = username_input
                    st.session_state.page = 'workspace'; st.rerun()
                else: st.error("Please enter both username and password.")
        
        st.write("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Forgot Password?", use_container_width=True): st.session_state.page = 'forgot'; st.rerun()
        with c2:
            if st.button("Sign Up", use_container_width=True): st.session_state.page = 'signup'; st.rerun()

        st.write("<hr style='border-color: rgba(255,255,255,0.08); margin: 10px 0 15px 0;'>", unsafe_allow_html=True)
        if st.button("Back to Welcome", use_container_width=True): st.session_state.page = 'welcome'; st.rerun()

def signup_page():
    st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-bottom: 0;'><span class='gradient-text'>Create Account</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A0A0AB; font-size: 1.1rem; margin-top: 10px; margin-bottom: 25px;'>Join the multi-agent ecosystem.</p>", unsafe_allow_html=True)
    _, col_center, _ = st.columns([1, 1.2, 1])
    with col_center:
        with st.form("signup_form"):
            st.markdown("<p style='font-size: 0.95rem; font-weight: 500; margin-bottom: 8px; color: #EDEDED;'>Full Name</p>", unsafe_allow_html=True)
            st.text_input("Name", value=st.session_state.user_name, label_visibility="collapsed")
            st.markdown("<p style='font-size: 0.95rem; font-weight: 500; margin-top: 20px; margin-bottom: 8px; color: #EDEDED;'>Create Password</p>", unsafe_allow_html=True)
            st.text_input("Password", type="password", label_visibility="collapsed")
            if st.form_submit_button("Register Account", use_container_width=True):
                st.success("Account created successfully! Redirecting...")
                time.sleep(1.5)
                st.session_state.page = 'login'; st.rerun()
                
        st.write("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        if st.button("Back to Login", use_container_width=True): st.session_state.page = 'login'; st.rerun()

def forgot_page():
    st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-bottom: 0;'><span class='gradient-text'>Reset Password</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A0A0AB; font-size: 1.1rem; margin-top: 10px; margin-bottom: 25px;'>Recover your system access.</p>", unsafe_allow_html=True)
    _, col_center, _ = st.columns([1, 1.2, 1])
    with col_center:
        with st.form("forgot_form"):
            st.markdown("<p style='font-size: 0.95rem; font-weight: 500; margin-bottom: 8px; color: #EDEDED;'>Username or Email</p>", unsafe_allow_html=True)
            st.text_input("Username", value=st.session_state.user_name, label_visibility="collapsed")
            if st.form_submit_button("Send Recovery Link", use_container_width=True):
                st.success("Recovery link sent to your email.")
                time.sleep(1.5)
                st.session_state.page = 'login'; st.rerun()
                
        st.write("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        if st.button("Back to Login", use_container_width=True): st.session_state.page = 'login'; st.rerun()

def display_history_widget():
    st.write("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
    if not st.session_state.history_data:
        st.markdown("<p style='color: #8A8A93;'>No active session history yet. Start a new chat!</p>", unsafe_allow_html=True)
    else:
        for topic in st.session_state.history_data:
            st.markdown('<div class="history-link-btn">', unsafe_allow_html=True)
            if st.button(topic, key=f"hist_{topic}"):
                st.toast(f"Loaded: {topic}")
            st.markdown('</div>', unsafe_allow_html=True)

def workspace_page():
    # --- TOP HEADER ROW ---
    c1, c2, c3, c4 = st.columns([12, 3, 3, 3])
    with c1:
        st.markdown(f"<h3 style='margin-top: 0px;'>🤖 <span class='gradient-text'>Multi Agent Chatbot</span> <span style='color: #8A8A93; font-size: 1rem; font-weight: 400;'>| User: {st.session_state.user_name}</span></h3>", unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="header-btn">', unsafe_allow_html=True)
        if st.button("History", use_container_width=True):
            st.session_state.history_view = not st.session_state.history_view
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="header-btn">', unsafe_allow_html=True)
        if st.button("New Chat", use_container_width=True): 
            st.session_state.messages = []
            st.session_state.edit_message_index = None
            st.session_state.edit_input_value = ""
            st.session_state.history_view = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="header-btn">', unsafe_allow_html=True)
        if st.button("Log out", use_container_width=True):
            st.session_state.page = 'welcome' 
            st.session_state.messages = []
            st.session_state.user_name = "" 
            st.session_state.edit_message_index = None
            st.session_state.edit_input_value = ""
            st.session_state.history_view = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin-top: 5px; margin-bottom: 25px;'>", unsafe_allow_html=True)

    if st.session_state.history_view:
        display_history_widget()
        return 

    display_agent = st.session_state.selected_agent

    # --- SELECTION DROPDOWNS ---
    col_header, col_attach, col_tools, col_model = st.columns([2, 1, 1.2, 1.2])
    
    with col_header:
        h_color = "#00e5ff"
        h_text = f"{display_agent} Environment"
        st.markdown(f"<h4 style='color: {h_color}; margin-top:5px; font-weight: 700; transition: all 0.3s ease;'>{h_text}</h4>", unsafe_allow_html=True)
    
    with col_attach:
        with st.popover("📎 Attach"):
            attach_type = st.radio("Select source:", ["Local Files", "Photos", "Google Drive Link", "Code Snippet", "NotebookLM Link"], label_visibility="collapsed")
            st.write("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            if attach_type == "Local Files":
                st.file_uploader("Upload text documents", accept_multiple_files=True, key="doc_uploads")
            elif attach_type == "Photos":
                st.file_uploader("Upload images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True, key="photo_uploads")
            elif attach_type == "Google Drive Link":
                st.text_input("Paste Shared Link", placeholder="https://drive.google.com/...")
                st.button("Link Document", key="drive_btn")
            elif attach_type == "Code Snippet":
                st.text_area("Paste your code here", height=150)
            elif attach_type == "NotebookLM Link":
                st.text_input("Paste Notebook URL", placeholder="https://notebooklm.google.com/...")
                st.button("Connect Notebook", key="notebook_btn")
                
    with col_tools:
        tool_options = [
            "Research Agent", "Writing Agent", "Code Agent", "Review Agent",
            "Deep Research", "Guided Learning"
        ]
        
        # --- FIX: NATIVE SELECTBOX (Auto-Closes instantly on selection) ---
        selected_tool_index = tool_options.index(st.session_state.selected_agent) if st.session_state.selected_agent in tool_options else 0
        st.session_state.selected_agent = st.selectbox(
            "Tools", 
            options=tool_options, 
            index=selected_tool_index, 
            label_visibility="collapsed"
        )
        
    with col_model:
        model_options = ["Fast (Answers quickly)", "Thinking (Solves complex problems)", "Pro (Advanced maths and code)"]
        
        # --- FIX: NATIVE SELECTBOX (Auto-Closes instantly on selection) ---
        selected_model_index = model_options.index(st.session_state.selected_model) if st.session_state.selected_model in model_options else 0
        st.session_state.selected_model = st.selectbox(
            "Models", 
            options=model_options, 
            index=selected_model_index, 
            label_visibility="collapsed"
        )

    # --- IN-PLACE RENDER CHAT HISTORY & EDIT UI ---
    for i, message in enumerate(st.session_state.messages):
        if st.session_state.edit_message_index == i:
            st.markdown("<div class='edit-mode-container'>", unsafe_allow_html=True)
            st.markdown("<p style='color: #00e5ff; font-weight: 600; margin-bottom: 10px;'>✎ Editing Message</p>", unsafe_allow_html=True)
            
            updated_prompt = st.text_area("Edit", value=st.session_state.edit_input_value, height=100, label_visibility="collapsed", key=f"edit_area_{i}")
            
            btn_col1, btn_col2, _ = st.columns([1.5, 1.5, 9])
            with btn_col1:
                st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                if st.button("Save", type="primary", key=f"save_{i}"):
                    st.session_state.messages[i]["content"] = updated_prompt
                    st.session_state.messages = st.session_state.messages[:i+1]
                    st.session_state.edit_message_index = None
                    st.session_state.pending_edit_generation = True
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                    
            with btn_col2:
                st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                if st.button("Cancel", key=f"cancel_{i}"):
                    st.session_state.edit_message_index = None
                    st.session_state.edit_input_value = ""
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        else:
            avatar_icon = "🔹" if message["role"] == "user" else "🤖"
            with st.chat_message(message["role"], avatar=avatar_icon):
                col_icon, col_text = st.columns([1, 15])
                with col_icon:
                    st.markdown('<div class="action-icons">', unsafe_allow_html=True)
                    if message["role"] == "user":
                        if st.session_state.edit_message_index is None:
                            if st.button("✎", key=f"ecosys_edit_{i}", help="Edit prompt"):
                                st.session_state.edit_message_index = i
                                st.session_state.edit_input_value = message["content"]
                                st.rerun()
                    else:
                        if st.button("📋", key=f"ecosys_copy_{i}", help="Copy response"):
                            st.toast("Response Copied", icon="📋")
                    st.markdown('</div>', unsafe_allow_html=True)
                with col_text:
                    st.markdown(message["content"])

    active_files = []
    if "doc_uploads" in st.session_state and st.session_state.doc_uploads:
        active_files.extend(st.session_state.doc_uploads)

    # --- HIGH-SPEED DIRECT GENERATION FLOW ---
    if st.session_state.edit_message_index is None and not st.session_state.pending_edit_generation:
        if prompt := st.chat_input(f"Ask {display_agent}..."):
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            if len(st.session_state.messages) <= 2: 
                topic = prompt[:35] + "..." if len(prompt) > 35 else prompt
                if topic not in st.session_state.history_data:
                    st.session_state.history_data.insert(0, topic)

            with st.chat_message("user", avatar="🔹"):
                c_icon, c_text = st.columns([1, 15])
                with c_icon:
                    st.markdown('<div class="action-icons">', unsafe_allow_html=True)
                    st.button("✎", key=f"ecosys_edit_temp")
                    st.markdown('</div>', unsafe_allow_html=True)
                with c_text:
                    if active_files:
                        st.markdown(f"*(Attached {len(active_files)} file(s))* \n**{prompt}**")
                    else:
                        st.markdown(prompt)

            with st.chat_message("assistant", avatar="🤖"):
                c_icon, c_text = st.columns([1, 15])
                with c_icon:
                    st.markdown('<div class="action-icons">', unsafe_allow_html=True)
                    st.button("📋", key=f"ecosys_copy_temp")
                    st.markdown('</div>', unsafe_allow_html=True)
                with c_text:
                    response = st.write_stream(run_agent_stream(st.session_state.selected_agent, prompt, st.session_state.selected_model, files=active_files))
            
            st.session_state.messages.append({"role": "assistant", "content": response})

    # --- PENDING EDIT GENERATION ROUTE ---
    if st.session_state.pending_edit_generation and len(st.session_state.messages) > 0:
        latest_prompt = st.session_state.messages[-1]["content"]
        
        with st.chat_message("assistant", avatar="🤖"):
            c_icon, c_text = st.columns([1, 15])
            with c_icon:
                st.markdown('<div class="action-icons">', unsafe_allow_html=True)
                st.button("📋", key=f"ecosys_copy_temp_edit")
                st.markdown('</div>', unsafe_allow_html=True)
            with c_text:
                response = st.write_stream(run_agent_stream(st.session_state.selected_agent, latest_prompt, st.session_state.selected_model, files=active_files))
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.pending_edit_generation = False

# --- 7. Router ---
if st.session_state.page == 'welcome': welcome_page()
elif st.session_state.page == 'login': login_page()
elif st.session_state.page == 'signup': signup_page()
elif st.session_state.page == 'forgot': forgot_page()
elif st.session_state.page == 'workspace': workspace_page()