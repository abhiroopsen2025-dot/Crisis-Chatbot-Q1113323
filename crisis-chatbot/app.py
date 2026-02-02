#!/usr/bin/env python3
"""Crisis Response Chatbot - Simple & Intuitive"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="Crisis Responder",
    page_icon="🚨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Styling
st.markdown("""
<style>
.stTextInput { margin-bottom: 10px; }
.chat-msg { padding: 10px; border-radius: 8px; margin: 8px 0; }
.chat-bot { background: #f0f0f0; color: #000; }
.chat-user { background: #d0e8ff; color: #000; }
.risk-critical { background: #ffe0e0; color: #cc0000; padding: 10px; border-radius: 5px; }
.risk-high { background: #fff4e0; color: #ff8800; padding: 10px; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# Intent classifier
INTENTS = {
    "earthquake": ["earthquake", "tremor", "quake", "shaking"],
    "flood": ["flood", "water", "flooding"],
    "fire": ["fire", "burning", "flames"],
    "injury": ["hurt", "injured", "bleeding"],
    "medical": ["ambulance", "heart", "chest pain"],
    "help": ["help", "assist"],
}

RESPONSES = {
    "earthquake": "🌍 Drop, cover, hold on! Move away from windows.",
    "flood": "💧 Move to higher ground immediately.",
    "fire": "🔥 Evacuate immediately to safety.",
    "injury": "🚑 Emergency team dispatched. Describe your injury.",
    "medical": "⚕️ Ambulance on the way. Stay calm.",
    "help": "🆘 I'm here to help. What's wrong?",
}

RISKS = {
    "earthquake": "🔴 CRITICAL",
    "flood": "🟠 HIGH",
    "fire": "🔴 CRITICAL",
    "injury": "🔴 CRITICAL",
    "medical": "🔴 CRITICAL",
}


def classify(text: str):
    """Classify intent"""
    text_lower = text.lower()
    best = "help"
    best_score = 0.1
    
    for intent, keywords in INTENTS.items():
        score = sum(1 for kw in keywords if kw in text_lower) / len(keywords)
        if score > best_score:
            best = intent
            best_score = score
    
    return best, best_score


# Main app
st.title("🚨 Crisis Response")
st.write("*Emergency assistance when you need it*")

# Init session
if "msgs" not in st.session_state:
    st.session_state.msgs = []

# Chat display
for msg in st.session_state.msgs:
    role = msg["role"]
    content = msg["content"]
    css_class = "chat-user" if role == "user" else "chat-bot"
    emoji = "👤" if role == "user" else "🤖"
    st.markdown(f'<div class="chat-msg {css_class}">{emoji} {content}</div>', unsafe_allow_html=True)

# Input form
with st.form("msg_form", clear_on_submit=True):
    user_msg = st.text_input("Describe emergency...", placeholder="e.g., There's a flood")
    submit = st.form_submit_button("Send", use_container_width=True)
    
    if submit and user_msg:
        st.session_state.msgs.append({"role": "user", "content": user_msg})
        
        intent, conf = classify(user_msg)
        response = RESPONSES.get(intent, "How can I help?")
        
        st.session_state.msgs.append({"role": "bot", "content": response})
        st.rerun()

# Actions
st.divider()
st.write("**Quick Help:**")

col1, col2 = st.columns(2)
with col1:
    if st.button("📍 Shelters", use_container_width=True, key="btn_shelter"):
        with st.container():
            st.toast("✅ Shelters found!")
            st.success("**Nearby Shelters:**\n• Community Center: 0.5km\n• School: 0.8km\n• Town Hall: 1.2km")

with col2:
    if st.button("🗺️ Routes", use_container_width=True, key="btn_routes"):
        with st.container():
            st.toast("✅ Routes calculated!")
            st.info("**Evacuation Routes:**\n• Route 1: 2.3km (12min)\n• Route 2: 3.1km (18min)")

col3, col4 = st.columns(2)
with col3:
    if st.button("🚑 Ambulance", use_container_width=True, key="btn_ambulance"):
        with st.container():
            st.toast("✅ Ambulance dispatch!")
            st.success("**Medical Response:**\n• ETA: 5 minutes\n• Hospital: 2km away")

with col4:
    if st.button("☎️ Operator", use_container_width=True, key="btn_operator"):
        with st.container():
            st.toast("✅ Operator connected!")
            st.info("**Live Support:**\n• Status: Connected\n• Operator: Ready to assist")

# Status
if st.session_state.msgs:
    last_user = None
    for msg in reversed(st.session_state.msgs):
        if msg["role"] == "user":
            last_user = msg["content"]
            break
    
    if last_user:
        intent, conf = classify(last_user)
        risk = RISKS.get(intent, "🟢 LOW")
        
        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("Intent", intent.upper())
        c2.metric("Confidence", f"{conf*100:.0f}%")
        c3.metric("Risk", risk)
