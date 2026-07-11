"""
MINI PROJECT — AI Personal Assistant Chatbot
Gen AI & ML Internship — Week 2

Features required:
  - Chat Interface
  - AI Responses
  - Prompt Templates (personas as system prompts)
  - Chat History
  - Streamlit UI

Run with: streamlit run mini_project_chatbot.py

Uses OpenAI's official SDK. API key is entered in the sidebar at runtime —
never hardcoded, never saved to disk.
"""

import streamlit as st
from openai import OpenAI, AuthenticationError, APIConnectionError, RateLimitError, APIError

st.set_page_config(page_title="AI Personal Assistant Chatbot", page_icon="🤖", layout="centered")

# ---------------------------------------------------------------------------
# PROMPT TEMPLATES (personas) — each is a system prompt
# ---------------------------------------------------------------------------
PERSONAS = {
    "General Assistant": (
        "You are a helpful, concise, and friendly general-purpose AI assistant. "
        "Answer clearly and ask clarifying questions when the request is ambiguous."
    ),
    "Senior Python Developer": (
        "You are a senior Python developer with 10+ years of experience. "
        "Give production-quality code, explain trade-offs briefly, and flag "
        "potential bugs or edge cases in any code you review."
    ),
    "Career Coach": (
        "You are an experienced career coach for students in tech. Be encouraging "
        "but honest, give actionable and specific advice, and keep answers structured."
    ),
    "Sarcastic Friend": (
        "You are a witty, sarcastic but ultimately helpful friend. Keep the sarcasm "
        "light and never actually unhelpful or mean-spirited."
    ),
    "Interview Prep Bot": (
        "You are a technical interviewer preparing candidates for software engineering "
        "roles. Ask one question at a time, give feedback on answers, and rate responses "
        "out of 10 with a brief justification."
    ),
    "Custom": "",  # user fills their own system prompt
}

# ---------------------------------------------------------------------------
# SIDEBAR — API key + persona selection
# ---------------------------------------------------------------------------
st.sidebar.header("🔑 OpenAI API Key")
api_key = st.sidebar.text_input(
    "Enter your OpenAI API key",
    type="password",
    help="Get one at platform.openai.com/api-keys",
)
st.sidebar.caption("Stored only in this session — never hardcoded or saved to disk.")

st.sidebar.header("🎭 Prompt Template (Persona)")
persona_name = st.sidebar.selectbox("Choose a persona", list(PERSONAS.keys()))

if persona_name == "Custom":
    system_prompt = st.sidebar.text_area(
        "Custom system prompt", value=st.session_state.get("custom_system_prompt", ""), height=150
    )
    st.session_state["custom_system_prompt"] = system_prompt
else:
    system_prompt = PERSONAS[persona_name]
    st.sidebar.text_area("System prompt (preview)", value=system_prompt, height=150, disabled=True)

temperature = st.sidebar.slider("Creativity (temperature)", 0.0, 1.5, 0.7, 0.1)

if st.sidebar.button("🗑️ Clear chat history"):
    st.session_state["chat_history"] = []
    st.rerun()

# ---------------------------------------------------------------------------
# MAIN — Chat Interface
# ---------------------------------------------------------------------------
st.title("🤖 AI Personal Assistant Chatbot")
st.caption("Mini Project · Gen AI & ML Internship · Powered by OpenAI gpt-4o-mini")

# --- Chat History (session_state) ---
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []  # list of {"role": ..., "content": ...}

# --- Render past messages ---
for msg in st.session_state["chat_history"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat input ---
user_input = st.chat_input("Type your message...")

if user_input:
    if not api_key:
        st.error("⚠️ Please enter your OpenAI API key in the sidebar first.")
    else:
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Full message list: system prompt + running history (context across turns)
        messages = [{"role": "system", "content": system_prompt}] + st.session_state["chat_history"]

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    client = OpenAI(api_key=api_key)
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=messages,
                        temperature=temperature,
                    )
                    reply = response.choices[0].message.content
                    st.markdown(reply)
                    st.session_state["chat_history"].append({"role": "assistant", "content": reply})

                except AuthenticationError:
                    st.error("❌ Authentication failed. Please check your OpenAI API key.")
                except RateLimitError:
                    st.error("❌ Rate limit or quota exceeded. Please try again later.")
                except APIConnectionError:
                    st.error("❌ Network error while connecting to OpenAI. Check your internet connection.")
                except APIError as e:
                    st.error(f"❌ OpenAI API error: {e}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {e}")
