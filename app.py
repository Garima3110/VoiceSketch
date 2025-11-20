import streamlit as st
import speech_recognition as sr
import streamlit.components.v1 as components
from generator import DesignGenerator

# --- CONFIG ---
st.set_page_config(page_title="VoiceSketch GenAI", page_icon="✨", layout="wide")

if 'generator' not in st.session_state:
    st.session_state['generator'] = DesignGenerator()
generator = st.session_state['generator']

# --- STYLES ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    h1 { background: linear-gradient(to right, #4F46E5, #9333EA); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800 !important; }
    .stButton>button { background: linear-gradient(to right, #4F46E5, #9333EA); color: white; border: none; font-weight: 600; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- AUDIO FUNCTION ---
def record_voice():
    r = sr.Recognizer()
    status_box = st.empty()
    try:
        with sr.Microphone() as source:
            status_box.info("🎤 Calibrating noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            status_box.warning("🔴 Listening...")
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            status_box.info("⏳ Sending to AI...")
            text = r.recognize_google(audio)
            status_box.empty()
            return text
    except OSError as e:
        # Catches the Mac 'Bad CPU type' error
        if "Bad CPU type" in str(e) or "Errno 86" in str(e):
            status_box.error("⚠️ Audio Error: Your Mac is missing the 'flac' tool.")
            st.warning("Please use the **Text Input** box on the right instead, or run `brew install flac` in your terminal to fix audio.")
        else:
            status_box.error(f"Microphone Error: {e}")
        return None
    except sr.UnknownValueError:
        status_box.error("Could not understand audio.")
    except Exception as e:
        status_box.error(f"Error: {e}")
    return None

# --- UI ---
with st.sidebar:
    st.title("⚙️ Setup")
    api_key = st.text_input("Gemini API Key", type="password")
    if api_key: st.success("✅ Key loaded!")

st.title("VoiceSketch ✨")
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎙️ Voice Input")
    if st.button("Start Recording"):
        if not api_key: st.error("Enter API Key first!")
        else:
            text = record_voice()
            if text:
                st.session_state['prompt'] = text
                st.success(f"Heard: {text}")

with col2:
    st.subheader("⌨️ Text Input")
    text_input = st.text_input("Type here:")
    if st.button("Generate"): st.session_state['prompt'] = text_input

if 'prompt' in st.session_state and st.session_state['prompt']:
    with st.spinner("🧠 Generating..."):
        html_code, status = generator.generate_code(st.session_state['prompt'], api_key)
    
    tab1, tab2 = st.tabs(["Preview", "Code"])
    with tab1: components.html(html_code, height=600, scrolling=True)
    with tab2: st.code(html_code, language="html")
