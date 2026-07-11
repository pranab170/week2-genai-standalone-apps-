"""
AI Summarizer — standalone
Uses the NEW google-genai SDK (`from google import genai`).

Run with: streamlit run ai_summarizer.py
"""

import streamlit as st
from google import genai

st.set_page_config(page_title="AI Summarizer", page_icon="📝", layout="centered")

st.sidebar.header("🔑 Gemini API Key")
api_key = st.sidebar.text_input("Enter your Gemini API key", type="password")
st.sidebar.caption("Stored only in this session — never hardcoded or saved to disk.")
model = st.sidebar.selectbox("Gemini model", ["gemini-1.5-flash", "gemini-1.5-pro"], index=0)

st.title("📝 AI Summarizer")
st.caption("Powered by Google Gemini · new google-genai SDK")

input_text = st.text_area(
    "Paste the text you want to summarize",
    placeholder="Paste an article, report, or any long text here...",
    height=250,
)
summary_style = st.radio(
    "Summary style", ["Concise paragraph", "Bullet points", "One-line TL;DR"], horizontal=True
)

summarize = st.button("📝 Summarize", type="primary")

if summarize:
    if not api_key:
        st.error("⚠️ Please enter your Gemini API key in the sidebar first.")
    elif not input_text.strip():
        st.warning("Please paste some text to summarize.")
    else:
        style_instruction = {
            "Concise paragraph": "Summarize the following text in a single concise paragraph.",
            "Bullet points": "Summarize the following text as clear, concise bullet points.",
            "One-line TL;DR": "Summarize the following text in a single, punchy one-line TL;DR.",
        }[summary_style]
        prompt = f"{style_instruction}\n\nText:\n{input_text}"

        with st.spinner("Summarizing with Gemini..."):
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(model=model, contents=prompt)
                result = getattr(response, "text", None)
                success = bool(result)
                if not success:
                    result = "❌ Gemini returned an empty response. Try rephrasing your prompt."
            except Exception as e:
                err_str = str(e)
                if "API key" in err_str or "PERMISSION" in err_str.upper() or "401" in err_str:
                    result = "❌ Authentication failed. Please check your Gemini API key."
                elif "404" in err_str or "NOT_FOUND" in err_str.upper():
                    result = f"❌ Model not found ({model}). It may have been deprecated or renamed."
                elif "RESOURCE_EXHAUSTED" in err_str.upper() or "429" in err_str:
                    result = "❌ Gemini quota/rate limit exceeded. Please try again later."
                else:
                    result = f"❌ Gemini API error: {err_str}"
                success = False

        st.divider()
        st.subheader("Summary")
        if success:
            st.markdown(result)
        else:
            st.error(result)
