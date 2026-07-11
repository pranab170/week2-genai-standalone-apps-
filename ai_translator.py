"""
AI Translator — standalone
Built using the OpenAI API (gpt-4o-mini).

Run with: streamlit run ai_translator.py
"""

import streamlit as st
from openai import OpenAI, AuthenticationError, APIConnectionError, RateLimitError, APIError

st.set_page_config(page_title="AI Translator", page_icon="🌐", layout="centered")

st.sidebar.header("🔑 OpenAI API Key")
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
st.sidebar.caption("Stored only in this session — never hardcoded or saved to disk.")

st.title("🌐 AI Translator")
st.caption("Powered by OpenAI · gpt-4o-mini")

LANGUAGES = [
    "English", "Hindi", "Odia", "Spanish", "French", "German",
    "Japanese", "Chinese (Simplified)", "Arabic", "Bengali", "Tamil", "Telugu",
]

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("From", ["Auto-detect"] + LANGUAGES, index=0)
with col2:
    target_lang = st.selectbox("To", LANGUAGES, index=1)

input_text = st.text_area("Text to translate", placeholder="Type or paste text here...", height=150)

translate = st.button("🌐 Translate", type="primary")

if translate:
    if not api_key:
        st.error("⚠️ Please enter your OpenAI API key in the sidebar first.")
    elif not input_text.strip():
        st.warning("Please enter some text to translate.")
    else:
        source_clause = "the source language (auto-detect it)" if source_lang == "Auto-detect" else source_lang
        system_prompt = (
            f"You are a professional translator. Translate text from {source_clause} to {target_lang}. "
            f"Preserve tone and meaning. Only output the translated text, with no extra commentary, "
            f"quotes, or explanation."
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]

        with st.spinner("Translating..."):
            try:
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini", messages=messages, temperature=0.3
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
        st.subheader(f"Translation ({target_lang})")
        if success:
            st.markdown(result)
        else:
            st.error(result)
