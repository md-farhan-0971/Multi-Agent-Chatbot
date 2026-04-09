import streamlit as st
import time
from agency.nodes import researcher_node, writer_node, editor_node

# --- Page Configuration ---
st.set_page_config(page_title="AI Content Agency", page_icon="⚡", layout="wide")

# --- Ultra-Premium CSS (Combined for all pages) ---
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1a2332 0%, #080b12 80%);
        color: #e6edf3;
    }
    #MainMenu, footer, header {visibility: hidden;}

    /* Hero Text */
    .hero-title { font-size: 3.5rem; font-weight: 700; text-align: center; margin-top: 5vh; }
    .hero-subtitle { font-size: 2rem; font-weight: 400; text-align: center; color: #8b949e; margin-bottom: 3rem; }

    /* Glassmorphism Input Bar (Home Page) */
    .chat-input-bar {
        background: rgba(22, 27, 34, 0.6);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 30px;
        max-width: 800px;
        margin: 0 auto 2rem auto;
    }

    /* Agent Cards (Workspace Page) */
    div[data-testid="stButton"] button {
        background: rgba(22, 27, 34, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        transition: all 0.3s ease;
        color: white;
    }
    div[data-testid="stButton"] button:hover {
        border-color: #00ffb2;
        transform: translateY(-5px);
    }
    .selected-card div[data-testid="stButton"] button {
        border: 2px solid #00ffb2 !important;
        background: rgba(0, 255, 178, 0.05) !important;
    }

    /* Primary Buttons (Login & Deploy) */
    .primary-cta div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #00ffb2 0%, #00b377 100%) !important;
        color: #040d12 !important;
        font-weight: 800;
        border-radius: 50px;
    }

    /* Output Box */
    .output-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 255, 178, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- State Management ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_agent' not in st.session_state:
    st.session_state.selected_agent = None
if 'agent_output' not in st.session_state:
    st.session_state.agent_output = None

# --- Backend Integration ---
def run_real_agent(agent_name, prompt):
    try:
        state_input = {"topic": prompt}
        if agent_name == "Researcher":
            res = researcher_node(state_input)
            raw = res.get("research_notes", "Empty")
        elif agent_name == "Writer":
            res = writer_node(state_input)
            raw = res.get("draft", "Empty")
        else:
            res = editor_node(state_input)
            raw = res.get("final_content", "Empty")
        
        return raw.split("\n\n", 1)[1] if "\n\n" in raw else raw
    except Exception as e:
        return f"Error: {str(e)}"

# ==========================================
# PAGE 1: HOME (Copilot Style)
# ==========================================
def home_page():
    st.markdown('<div class="hero-title">Good evening</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">What can I help you with today?</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chat-input-bar">', unsafe_allow_html=True)
    st.text_area("Ask anything...", height=100, placeholder="Describe your project or ask a question...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div class="primary-cta">', unsafe_allow_html=True)
        if st.button("Enter Agency Workspace 🚀", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 2: LOGIN
# ==========================================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("")
        with st.form("login_form"):
            st.markdown("<h2 style='text-align: center;'>Agency Access</h2>", unsafe_allow_html=True)
            email = st.text_input("Work Email")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Authorize Access 🔐", use_container_width=True):
                if email and password:
                    st.session_state.page = 'workspace'
                    st.rerun()

# ==========================================
# PAGE 3: WORKSPACE
# ==========================================
def workspace_page():
    col_l, col_r = st.columns([4, 1])
    col_l.markdown("<h2>⚡ Content<span style='color: #00ffb2;'>Agency</span></h2>", unsafe_allow_html=True)
    if col_r.button("🚪 Logout"):
        st.session_state.page = 'home'
        st.rerun()

    st.write("---")
    c1, c2, c3 = st.columns(3)
    
    agents = {
        "Researcher": "🔍\n\n### Researcher\n\nFact-finding & data extraction.",
        "Writer": "✍️\n\n### Writer\n\nCreative drafting & storytelling.",
        "Editor": "🧐\n\n### Editor\n\nPolishing & quality control."
    }

    for i, (name, desc) in enumerate(agents.items()):
        with [c1, c2, c3][i]:
            if st.session_state.selected_agent == name:
                st.markdown("<div class='selected-card'>", unsafe_allow_html=True)
            if st.button(desc, key=name, use_container_width=True):
                st.session_state.selected_agent = name
                st.session_state.agent_output = None
                st.rerun()
            if st.session_state.selected_agent == name:
                st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.selected_agent:
        prompt = st.text_area(f"Parameters for {st.session_state.selected_agent}:", height=100)
        if st.button(f"Deploy {st.session_state.selected_agent} ⚡"):
            with st.spinner("Processing..."):
                st.session_state.agent_output = run_real_agent(st.session_state.selected_agent, prompt)
        
        if st.session_state.agent_output:
            with st.chat_message("assistant", avatar="⚡"):
                st.markdown(st.session_state.agent_output)

# --- Routing ---
if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'login':
    login_page()
else:
    workspace_page()