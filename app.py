import streamlit as st
import requests
import base64
import time

# ─────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Video Generator 🎬",
    page_icon="🎬",
    layout="centered"
)

st.markdown("""
<style>
body { background-color: #0e0e0e; }
.stButton>button {
    background: linear-gradient(135deg, #ff6b00, #ffcc00);
    color: black !important;
    font-weight: bold;
    border-radius: 10px;
    font-size: 16px;
    border: none;
    width: 100%;
}
.stButton>button:hover { opacity: 0.9; transform: scale(1.01); }
.title-text {
    font-size: 2.4rem;
    font-weight: 900;
    background: linear-gradient(135deg, #ff6b00, #ffcc00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
}
.step-card {
    background: #1a1a2e;
    border-left: 4px solid #ff6b00;
    padding: 0.8rem 1rem;
    border-radius: 8px;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────────────
st.markdown('<div class="title-text">🎬 AI Sage Video Generator</div>', unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#aaa'>Topic likho → Script bane → Voice bane → Talking Video bane</p>",
    unsafe_allow_html=True
)
st.divider()

# ─────────────────────────────────────────────────────
#  SIDEBAR — API KEYS
# ─────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ API Keys")
    st.caption("Sab FREE hain — links niche hain 👇")

    anthropic_key = st.text_input("🤖 Anthropic Key", type="password", placeholder="sk-ant-...")
    elevenlabs_key = st.text_input("🔊 ElevenLabs Key", type="password", placeholder="abc123...")
    did_key = st.text_input("🎥 D-ID Key", type="password", placeholder="Base64 encoded key")

    st.divider()
    st.markdown("**🆓 Free Signup Links:**")
    st.markdown("• [Anthropic Console](https://console.anthropic.com)")
    st.markdown("• [ElevenLabs](https://elevenlabs.io)")
    st.markdown("• [D-ID Studio](https://studio.d-id.com)")
    st.markdown("• [Leonardo AI (Images)](https://app.leonardo.ai)")
    st.divider()
    st.markdown("**📘 Kaise use karein?**")
    st.markdown("""
    1. Upar ki 3 APIs signup karo
    2. Keys yahan daalo  
    3. Topic type karo
    4. Buttons press karo
    5. Video download karo!
    """)

# ─────────────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────────────
for key in ["script", "audio_bytes", "video_url"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ─────────────────────────────────────────────────────
#  STEP 1 — TOPIC + SETTINGS
# ─────────────────────────────────────────────────────
st.markdown("### 📝 Step 1 — Topic & Settings")

topic = st.text_input(
    "Video ka topic kya hai?",
    placeholder="e.g.  Stress aur pet ka connection | Subah khali pet pani pine ke fayde"
)

col1, col2 = st.columns(2)
with col1:
    duration = st.selectbox("Duration", ["30 seconds (~3-4 lines)", "45 seconds (~5-6 lines)", "60 seconds (~7-8 lines)"])
with col2:
    language = st.selectbox("Script Language", ["Hindi (हिंदी)", "Hinglish", "English"])

image_url = st.text_input(
    "🖼️ Character Image URL (Leonardo AI se banao)",
    placeholder="https://cdn.leonardo.ai/... ya koi bhi portrait image ka direct URL",
    help="Leonardo AI pe jaao → Ancient Indian Sage prompt daalo → Image URL copy karo"
)

st.caption("💡 **Agar image URL nahi hai:** Leonardo AI (free) pe signup karo, prompt: *'Ancient Indian rishi, muscular, rudraksha beads, dhoti, cinematic, 4K portrait'*")

st.divider()

# ─────────────────────────────────────────────────────
#  STEP 2 — SCRIPT GENERATION
# ─────────────────────────────────────────────────────
st.markdown("### 🤖 Step 2 — AI Script Generate Karo")

def generate_script(topic, duration, language, api_key):
    dur_seconds = duration.split(" ")[0]

    lang_map = {
        "Hindi (हिंदी)": "Pure Hindi in Devanagari script",
        "Hinglish": "Hinglish (Hindi words in Roman script mixed with English)",
        "English": "Simple clear English"
    }

    prompt = f"""You are writing a YouTube Shorts script for an ancient Indian sage (Rishi) character.
The sage speaks about health and wellness topics with wisdom and authority.

Topic: {topic}
Duration: {dur_seconds} seconds
Language: {lang_map[language]}

Rules:
- Write ONLY the spoken words — no stage directions
- Start with a powerful hook (question or shocking fact)
- 2-3 key insights in the middle
- End with a memorable conclusion
- Conversational, not lecture-style
- Sound like an ancient wise sage, not a doctor

Write the script now:"""

    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-opus-4-5",
            "max_tokens": 600,
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    if resp.status_code == 200:
        return resp.json()["content"][0]["text"].strip()
    else:
        st.error(f"Anthropic API Error: {resp.status_code} — {resp.text}")
        return None

if st.button("✨ Script Generate Karo"):
    if not topic:
        st.warning("⚠️ Pehle topic type karo!")
    elif not anthropic_key:
        st.warning("⚠️ Sidebar mein Anthropic API Key daalo!")
    else:
        with st.spinner("🤖 Claude AI script likh raha hai..."):
            result = generate_script(topic, duration, language, anthropic_key)
            if result:
                st.session_state.script = result

if st.session_state.script:
    st.success("✅ Script ready hai!")
    st.session_state.script = st.text_area(
        "📜 Script (Edit bhi kar sakte ho):",
        value=st.session_state.script,
        height=220
    )

st.divider()

# ─────────────────────────────────────────────────────
#  STEP 3 — VOICE GENERATION
# ─────────────────────────────────────────────────────
st.markdown("### 🔊 Step 3 — AI Voice Banao (ElevenLabs)")

voice_options = {
    "Deep Male (Sage jaisi awaaz)": "pNInz6obpgDQGcFmaJgB",
    "Strong Male": "VR6AewLTigWG4xSOukaG",
    "Calm Narrator": "yoZ06aMxZJJ28mfd3POQ"
}
selected_voice = st.selectbox("Voice Style:", list(voice_options.keys()))

def generate_voice(script, voice_id, api_key):
    resp = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        },
        json={
            "text": script,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.85,
                "style": 0.35,
                "use_speaker_boost": True
            }
        }
    )
    if resp.status_code == 200:
        return resp.content
    else:
        st.error(f"ElevenLabs Error: {resp.status_code} — {resp.text}")
        return None

if st.button("🔊 Voice Generate Karo"):
    if not st.session_state.script:
        st.warning("⚠️ Pehle script generate karo!")
    elif not elevenlabs_key:
        st.warning("⚠️ Sidebar mein ElevenLabs API Key daalo!")
    else:
        with st.spinner("🔊 AI voice ban rahi hai..."):
            voice_id = voice_options[selected_voice]
            audio = generate_voice(st.session_state.script, voice_id, elevenlabs_key)
            if audio:
                st.session_state.audio_bytes = audio

if st.session_state.audio_bytes:
    st.success("✅ Voice ready hai!")
    st.audio(st.session_state.audio_bytes, format="audio/mp3")
    st.download_button(
        "⬇️ Voice (MP3) Download Karo",
        data=st.session_state.audio_bytes,
        file_name="sage_voice.mp3",
        mime="audio/mp3"
    )

st.divider()

# ─────────────────────────────────────────────────────
#  STEP 4 — VIDEO GENERATION (D-ID)
# ─────────────────────────────────────────────────────
st.markdown("### 🎥 Step 4 — Talking Video Banao (D-ID)")
st.caption("Image + Voice = Talking Video ✨")

def create_talking_video(image_url, audio_bytes, api_key):
    # Audio ko base64 mein convert karo
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    # D-ID talk create karo
    resp = requests.post(
        "https://api.d-id.com/talks",
        headers={
            "Authorization": f"Basic {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "source_url": image_url,
            "script": {
                "type": "audio",
                "audio_url": f"data:audio/mpeg;base64,{audio_b64}"
            },
            "config": {
                "fluent": True,
                "pad_audio": 0.0,
                "stitch": True
            }
        }
    )

    if resp.status_code == 201:
        return resp.json().get("id")
    else:
        st.error(f"D-ID Error: {resp.status_code} — {resp.text}")
        return None

def poll_video_status(talk_id, api_key):
    headers = {"Authorization": f"Basic {api_key}"}
    progress = st.progress(0)
    status_text = st.empty()

    for i in range(40):
        resp = requests.get(f"https://api.d-id.com/talks/{talk_id}", headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            status = data.get("status")
            progress.progress(min((i + 1) * 5, 95))
            status_text.info(f"⏳ Status: {status} ({i*3} sec)")

            if status == "done":
                progress.progress(100)
                status_text.success("✅ Video ready!")
                return data.get("result_url")
            elif status == "error":
                status_text.error("❌ D-ID processing error")
                return None
        time.sleep(3)

    status_text.error("⌛ Timeout — dobara try karo")
    return None

if st.button("🎬 Talking Video Banao!"):
    if not st.session_state.audio_bytes:
        st.warning("⚠️ Pehle voice generate karo!")
    elif not image_url:
        st.warning("⚠️ Character image URL daalo!")
    elif not did_key:
        st.warning("⚠️ Sidebar mein D-ID API Key daalo!")
    else:
        with st.spinner("🎬 D-ID pe video bhejna..."):
            talk_id = create_talking_video(image_url, st.session_state.audio_bytes, did_key)

        if talk_id:
            st.info(f"📨 Video submitted! ID: `{talk_id}`")
            video_url = poll_video_status(talk_id, did_key)
            if video_url:
                st.session_state.video_url = video_url

if st.session_state.video_url:
    st.success("🎉 VIDEO READY HAI!")
    st.video(st.session_state.video_url)
    st.markdown(f"### 📥 [Video Download Karo]({st.session_state.video_url})")
    st.balloons()

# ─────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center;color:#444;font-size:12px'>Made with ❤️ | Claude AI + ElevenLabs + D-ID</p>",
    unsafe_allow_html=True
)
