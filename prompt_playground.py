"""
Prompt Playground — standalone
Test different system prompts and user prompts against OpenAI.

Run with: streamlit run prompt_playground.py
"""

import streamlit as st
from openai import OpenAI, AuthenticationError, APIConnectionError, RateLimitError, APIError

st.set_page_config(page_title="Prompt Playground", page_icon="🧪", layout="centered")

st.sidebar.header("🔑 OpenAI API Key")
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
st.sidebar.caption("Stored only in this session — never hardcoded or saved to disk.")

st.title("🧪 Prompt Playground")
st.caption("Experiment with system + user prompts · OpenAI gpt-4o-mini")

col1, col2 = st.columns(2)
with col1:
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"], index=0)
with col2:
    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)

system_prompt = st.text_area(
    "System Prompt",
    placeholder="e.g. You are a helpful assistant that only responds in bullet points.",
    height=120,
)

user_prompt = st.text_area(
    "User Prompt",
    placeholder="e.g. Explain quantum computing to a 10-year-old.",
    height=150,
)

run = st.button("▶️ Run Prompt", type="primary")

if "playground_history" not in st.session_state:
    st.session_state["playground_history"] = []

if run:
    if not api_key:
        st.error("⚠️ Please enter your OpenAI API key in the sidebar first.")
    elif not user_prompt.strip():
        st.warning("Please enter a user prompt.")
    else:
        messages = []
        if system_prompt.strip():
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})

        with st.spinner("Generating response..."):
            try:
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model=model, messages=messages, temperature=temperature
                )
                result = response.choices[0].message.content
                success = True
            except AuthenticationError:
                result, success = "❌ Authentication failed. Please check your OpenAI API key.", False
            except RateLimitError:
                result, success = "❌ Rate limit or quota exceeded. Please try again later.", False
            except APIConnectionError:
                result, success = "❌ Network error while connecting to OpenAI.", False
            except APIError as e:
                result, success = f"❌ OpenAI API error: {e}", False
            except Exception as e:
                result, success = f"❌ Unexpected error: {e}", False

        st.divider()
        st.subheader("Output")
        if success:
            st.markdown(result)
        else:
            st.error(result)

        st.session_state["playground_history"].insert(0, {
            "system": system_prompt, "user": user_prompt, "output": result, "success": success,
        })

if st.session_state.get("playground_history"):
    with st.expander(f"📜 Past runs ({len(st.session_state['playground_history'])})"):
        for i, run_item in enumerate(st.session_state["playground_history"]):
            st.markdown(f"**Run {i+1}**")
            st.text(f"System: {run_item['system'] or '(none)'}")
            st.text(f"User: {run_item['user']}")
            st.markdown(f"Output: {run_item['output']}")
            st.divider()
