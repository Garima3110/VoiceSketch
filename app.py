import streamlit as st
import speech_recognition as sr
import streamlit.components.v1 as components
from generator import DesignGenerator

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="VoiceSketch AI", 
    page_icon="🎨", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Backend
if 'generator' not in st.session_state:
    st.session_state['generator'] = DesignGenerator()
generator = st.session_state['generator']

# --- ENHANCED CUSTOM CSS ---
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

    /* Global Styles */
    * { font-family: 'Poppins', sans-serif; }
    
    /* Main Background - Dark Deep Space Theme */
    .stApp {
        background: radial-gradient(circle at top left, #1e1b4b, #0f172a);
        color: #ffffff;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }

    /* Header Styling */
    .main-header {
        text-align: center;
        padding: 40px 0;
        background: linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(0,0,0,0) 100%);
        margin-bottom: 30px;
        border-radius: 0 0 20px 20px;
    }
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #818cf8, #c084fc, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .tagline {
        font-size: 1.2rem;
        color: #94a3b8;
        font-weight: 300;
        letter-spacing: 1px;
        margin-top: 10px;
    }

    /* Custom Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        letter-spacing: 0.5px;
        width: 100%;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
        transform: scale(1.02);
    }

    /* Text Input Styling */
    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: white;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 10px 15px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #818cf8;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2);
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px;
        color: #94a3b8;
        padding: 10px 20px;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #6366f1;
        color: white;
    }

    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- HELPER: LOCAL RECORDING ---
def record_voice():
    """Records audio from the local machine's microphone"""
    r = sr.Recognizer()
    status_box = st.empty()
    
    try:
        with sr.Microphone() as source:
            status_box.info("🎤 Calibrating noise... please wait.")
            r.adjust_for_ambient_noise(source, duration=1)
            
            status_box.warning("🔴 Listening... Speak your vision!")
            
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            
            status_box.info("⏳ Processing speech...")
            text = r.recognize_google(audio)
            status_box.empty()
            return text
            
    except OSError:
        st.error("⚠️ Microphone error (Bad CPU type). Please use text input.")
        return None
    except sr.WaitTimeoutError:
        status_box.warning("No speech detected. Try again.")
    except sr.UnknownValueError:
        status_box.error("Could not understand audio.")
    except Exception as e:
        status_box.error(f"Error: {e}")
    return None

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Controls")
    
    st.markdown("### 🔑 API Access")
    api_key = st.text_input("Gemini API Key", type="password", placeholder="Paste key here...")
    
    if api_key:
        st.success("System Online")
    else:
        st.warning("API Key Required")
        st.markdown("[Get Free Key](https://aistudio.google.com/)", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💡 Pro Tips")
    st.caption("Try saying:")
    st.markdown("""
    - *"A cyberpunk dashboard with neon charts"*
    - *"A minimalist login page in pastel colors"*
    - *"A restaurant menu with image cards"*
    """)
    
    st.markdown("---")
    st.caption("v2.0 | Built with Streamlit & Gemini")

# --- MAIN HEADER ---
st.markdown("""
    <div class="main-header">
        <h1 class="main-title">VoiceSketch 🎨</h1>
        <p class="tagline">Your Voice, Visualized.</p>
    </div>
""", unsafe_allow_html=True)

# --- INPUT SECTION ---
# Removed the "input-card" div wrappers to remove the boxes
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 🎙️ Voice Command")
    if st.button("Start Recording 🎤", use_container_width=True):
        if not api_key:
            st.error("⚠️ Please enter your API Key in the sidebar.")
        else:
            text = record_voice()
            if text:
                st.session_state['prompt'] = text
                st.success(f"Recognized: '{text}'")

with col2:
    st.markdown("### ⌨️ Text Command")
    text_input = st.text_input("Describe your UI...", placeholder="e.g. A dark themed pricing table", label_visibility="collapsed")
    if st.button("Generate Code 🚀", use_container_width=True):
        st.session_state['prompt'] = text_input

# --- GENERATION SECTION ---
if 'prompt' in st.session_state and st.session_state['prompt']:
    user_prompt = st.session_state['prompt']
    
    st.markdown("---")
    st.markdown(f"### 🏗️ creating: *{user_prompt}*")
    
    with st.spinner("🧠 AI is architecting your design..."):
        html_code, status = generator.generate_code(user_prompt, api_key)
    
    # Tabs for Result
    tab1, tab2 = st.tabs(["📱 Interactive Preview", "💻 Source Code"])
    
    with tab1:
        # Add a white background wrapper for the preview so it doesn't blend into dark theme
        components.html(html_code, height=700, scrolling=True)
    
    with tab2:
        st.code(html_code, language="html")
        col_d1, col_d2 = st.columns([1,4])
        with col_d1:
            st.download_button(
                label="Download .html", 
                data=html_code, 
                file_name="voicesketch_design.html", 
                mime="text/html"
            )
