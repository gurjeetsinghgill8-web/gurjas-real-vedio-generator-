import streamlit as st
import requests
import base64
import asyncio
import tempfile
import os
import edge_tts

st.set_page_config(page_title="AI Video Generator 🎬", page_icon="🎬", layout="centered")

st.markdown("""
<style>
.stButton>button {
    background: linear-gradient(135deg, #ff6b00, #ffcc00);
    color: black !important; font-weight: bold;
    border-radius: 10px; font-size: 16px; border: none; width: 100%;
}
.title-text {
    font-size: 2.2rem; font-weight: 900;
    background: linear-gradient(135deg, #ff6b00, #ffcc00);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-text">🎬 AI Sage Video Generator</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#aaa'>100% FREE • No Credit Card • No Paid APIs</p>", unsafe_allow_html=True)
st.divider()

# SIDEBAR
with st.sidebar:
    st.header("⚙️ Setup")
    st.markdown("### 🔑 Sirf 1 Free Key Chahiye")
    gemini_key = st.text_input("🤖 Google Gemini Key", type="password", placeholder="AIza...")
    st.markdown("👉 [FREE key yahan se lo](https://aistudio.google.com/app/apikey) — No CC!")
    st.divider()
    st.markdown("**✅ Sab FREE hai:**")
    st.markdown("• Script → Google Gemini ✅\n• Voice → Microsoft Edge TTS ✅\n• Video → Hedra.com ✅")
    st.divider()
    voice_choice = st.selectbox("Hindi Voice:", [
        "hi-IN-MadhurNeural",
        "hi-IN-SwaraNeural",
        "hi-IN-AaravNeural",
    ])

# SESSION STATE
for k in ["script", "audio_bytes"]:
    if k not in st.session_state:
        st.session_state[k] = None

# STEP 1
st.markdown("### 📝 Step 1 — Topic Likho")
topic = st.text_input("Video ka topic:", placeholder="e.g. Stress aur pet ka connection | Subah pani pine ke fayde")
col1, col2 = st.columns(2)
with col1:
    duration = st.selectbox("Duration", ["30 seconds", "45 seconds", "60 seconds"])
with col2:
    language = st.selectbox("Language", ["Hindi", "Hinglish", "English"])
st.divider()

# STEP 2 - GEMINI SCRIPT
st.markdown("### 🤖 Step 2 — Script (Google Gemini — FREE)")

def generate_script(topic, duration, language, api_key):
    secs = duration.split()[0]
    lang_map = {
        "Hindi": "Pure Hindi in Devanagari script",
        "Hinglish": "Hinglish Roman script Hindi-English mix",
        "English": "Simple clear English"
    }
    prompt = f"""Write a YouTube Shorts script for an ancient Indian sage/rishi character.
Topic: {topic}
Duration: {secs} seconds (~{int(int(secs)/3)} sentences)
Language: {lang_map[language]}

Rules: ONLY spoken words, no stage directions, start with hook, end with strong conclusion, wise sage tone.
Script:"""

    resp = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
        headers={"Content-Type": "application/json"},
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )
    if resp.status_code == 200:
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    else:
        st.error(f"Gemini Error {resp.status_code}: {resp.text}")
        return None

if st.button("✨ Script Generate Karo"):
    if not topic:
        st.warning("⚠️ Topic type karo!")
    elif not gemini_key:
        st.warning("⚠️ Sidebar mein Gemini key daalo!")
    else:
        with st.spinner("🤖 Gemini AI likh raha hai..."):
            result = generate_script(topic, duration, language, gemini_key)
            if result:
                st.session_state.script = result

if st.session_state.script:
    st.success("✅ Script ready!")
    st.session_state.script = st.text_area("📜 Script (Edit bhi kar sakte ho):", value=st.session_state.script, height=200)

st.divider()

# STEP 3 - EDGE TTS VOICE
st.markdown("### 🔊 Step 3 — Voice (Microsoft Edge TTS — FREE, No Key!)")

async def make_voice(text, voice, path):
    comm = edge_tts.Communicate(text, voice)
    await comm.save(path)

def tts(text, voice):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        tmp = f.name
    asyncio.run(make_voice(text, voice, tmp))
    with open(tmp, "rb") as f:
        data = f.read()
    os.unlink(tmp)
    return data

if st.button("🔊 Voice Banao (FREE — No Key Needed!)"):
    if not st.session_state.script:
        st.warning("⚠️ Pehle script banao!")
    else:
        with st.spinner("🔊 Microsoft voice ban rahi hai..."):
            try:
                audio = tts(st.session_state.script, voice_choice)
                st.session_state.audio_bytes = audio
            except Exception as e:
                st.error(f"Error: {e}")

if st.session_state.audio_bytes:
    st.success("✅ Voice ready!")
    st.audio(st.session_state.audio_bytes, format="audio/mp3")
    st.download_button("⬇️ Voice MP3 Download Karo", data=st.session_state.audio_bytes,
                       file_name="sage_voice.mp3", mime="audio/mp3")

st.divider()

# STEP 4 - HEDRA (FREE MANUAL)
st.markdown("### 🎥 Step 4 — Talking Video (Hedra.com — FREE)")

st.info("✅ Hedra = 3 free videos/month, No Credit Card, No Signup hassle")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**🖼️ Image ke liye:**")
    st.markdown("[Ideogram.ai](https://ideogram.ai) — FREE, No CC")
    st.code("""Ancient Indian rishi sage, 
muscular, rudraksha beads, 
white dhoti, tilak forehead, 
ancient hut, cinematic 4K""", language="text")

with col2:
    st.markdown("**🎬 Video ke liye:**")
    st.markdown("[Hedra.com](https://www.hedra.com) — FREE")
    st.markdown("""
1. Hedra.com pe jaao
2. Sign Up (No CC)
3. Voice MP3 upload karo ↑
4. Image upload karo
5. Generate & Download!
""")

st.divider()
st.markdown("<p style='text-align:center;color:#444;font-size:12px'>100% FREE • Google Gemini + Edge TTS + Hedra</p>", unsafe_allow_html=True)
