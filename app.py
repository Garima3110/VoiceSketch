import streamlit as st
import speech_recognition as sr
import streamlit.components.v1 as components
from generator import DesignGenerator
import sys
import os

# --- SETUP ---
st.set_page_config(
    page_title="VoiceSketch", 
    page_icon="🎨", 
    layout="wide"
)

# Initialize the backend generator
if 'generator' not in st.session_state:
    st.session_state['generator'] = DesignGenerator()

generator = st.session_state['generator']

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp { background-color: #F3F4F6; font-family: 'Helvetica Neue', sans-serif; }
    h1, h2, h3, .stMarkdown, .stText { color: #000000 !important; }
    .stButton>button {
        background: linear-gradient(to right, #2563EB, #3B82F6);
        color: white; border: none; border-radius: 8px; padding: 0.6rem 1.2rem; font-weight: 600;
    }
    div[data-testid="stSidebar"] { background-color: #1F2937; }
    .right-header {
        background: #FFFFFF; padding: 6px 12px; border-radius: 10px;
        border: 1px solid #E5E7EB; display: inline-block; color: #111827; font-weight: 700;
    }
    div[data-testid="stSidebar"] .sidebar-top, 
    div[data-testid="stSidebar"] h1, div[data-testid="stSidebar"] h3, div[data-testid="stSidebar"] p {
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---

def record_voice():
    """Handles microphone input and speech-to-text with error handling for M1/M2 Macs"""
    r = sr.Recognizer()
    status_placeholder = st.empty()
    
    try:
        with sr.Microphone() as source:
            status_placeholder.info("🎤 Calibrating noise... please wait.")
            r.adjust_for_ambient_noise(source, duration=1)
            
            status_placeholder.warning("🔴 Listening now! Speak your command...")
            
            # Listen
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            status_placeholder.info("⏳ Processing audio...")
            
            # Recognize
            text = r.recognize_google(audio)
            status_placeholder.empty()
            return text
            
    except OSError as e:
        # Catch the specific Bad CPU type error (Errno 86)
        if "Bad CPU type" in str(e) or "[Errno 86]" in str(e):
            status_placeholder.error("❌ System Error: Missing 'flac' for Mac.")
            st.error("""
            **Mac (M1/M2/M3) Fix Required:**
            The SpeechRecognition library uses an old binary incompatible with Apple Silicon.
            
            Please run this in your terminal:
            ```bash
            brew install flac
            ```
            If that doesn't work, locate the `flac-mac` file in your error path and delete it to force Python to use the system flac.
            """)
            return None
        else:
            status_placeholder.error(f"System Error: {e}")
            return None
            
    except sr.WaitTimeoutError:
        status_placeholder.error("No speech detected. Try again.")
        return None
    except sr.UnknownValueError:
        status_placeholder.error("Could not understand audio.")
        return None
    except sr.RequestError:
        status_placeholder.error("Internet connection required.")
        return None
    except Exception as e:
        status_placeholder.error(f"Unexpected Error: {e}")
        return None

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-top">
            <h1 style="margin:0;">VoiceSketch 🎨</h1>
            <hr style="border:none;border-top:1px solid rgba(255,255,255,0.12);margin:8px 0 12px;">
            <h3 style="margin:0 0 6px 0;">Project Context</h3>
        </div>
        """, unsafe_allow_html=True)

    platform = st.selectbox("Platform", ["Web App (Responsive)", "Mobile (iOS)", "Tablet"]) 
    st.markdown("<h3 style='color:white; margin-top:10px;'>Accessibility</h3>", unsafe_allow_html=True)
    high_contrast = st.checkbox("Check Contrast Ratios", value=True)
    screen_reader = st.checkbox("Optimize for Screen Readers", value=True)

    st.markdown("---")
    st.markdown("""
        <div style="color:white">
            <h3>💡 How to use</h3>
            <ol>
                <li>Click <strong>Start Recording</strong></li>
                <li>Say: <em>"Create a login screen in purple"</em></li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

# --- MAIN APP CONTENT ---
col_header_1, col_header_2 = st.columns([3, 1])
with col_header_1:
    st.title("Voice-to-Visual Prototyping")
with col_header_2:
    st.markdown("<div class='right-header'>VS</div>", unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🎤 Input Command")
    
    if st.button("🎙️ Start Recording", use_container_width=True):
        voice_text = record_voice()
        if voice_text:
            st.success(f"Heard: {voice_text}")
            st.session_state['prompt'] = voice_text
    
    st.markdown("""<div style="text-align: center; margin: 10px 0;">— OR —</div>""", unsafe_allow_html=True)
    
    text_input = st.text_input("Type requirements manually", placeholder="e.g. Login page with blue buttons")
    if st.button("Generate from Text", use_container_width=True):
        st.session_state['prompt'] = text_input

with col2:
    st.subheader("📝 Transcript")
    if 'prompt' in st.session_state:
        st.info(f"**Command:** {st.session_state['prompt']}")
    else:
        st.info("Waiting for input...")

# OUTPUT
if 'prompt' in st.session_state and st.session_state['prompt']:
    st.markdown("---")
    with st.spinner("🤖 AI is sketching..."):
        html_code, component_type = generator.generate_code(st.session_state['prompt'])
    
    st.subheader(f"🎨 Result: {component_type}")
    
    tab_preview, tab_code = st.tabs(["📱 Live Preview", "💻 Generated Code"])
    
    with tab_preview:
        components.html(html_code, height=600, scrolling=True)
        
    with tab_code:
        st.code(html_code, language="html")
        st.download_button("📥 Download HTML", data=html_code, file_name="mockup.html", mime="text/html")