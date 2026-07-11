"""
AI Text Generator — standalone
Uses the NEW google-genai SDK (`from google import genai`), NOT the deprecated
google.generativeai package.

Run with: streamlit run ai_text_generator.py
"""

import streamlit as st
from google import genai

st.set_page_config(page_title="AI Text Generator", page_icon="✨", layout="centered")

st.sidebar.header("🔑 Gemini API Key")
api_key = st.sidebar.text_input("Enter your Gemini API key", type="password")
st.sidebar.caption("Stored only in this session — never hardcoded or saved to disk.")
model = st.sidebar.selectbox("Gemini model", ["gemini-1.5-flash", "gemini-1.5-pro"], index=0)

st.title("✨ AI Text Generator")
st.caption("Powered by Google Gemini · new google-genai SDK")

content_type = st.selectbox(
    "What do you want to generate?",
    ["Blog Post", "Product Description", "Email", "Social Media Caption", "Story", "Custom"],
)
topic = st.text_area("Topic / Details", placeholder="e.g. A blog post about the benefits of morning walks", height=120)
tone = st.selectbox("Tone", ["Professional", "Casual", "Persuasive", "Friendly", "Witty"])
length = st.select_slider("Approximate length", options=["Short", "Medium", "Long"], value="Medium")

generate = st.button("✨ Generate Text", type="primary")

if generate:
    if not api_key:
        st.error("⚠️ Please enter your Gemini API key in the sidebar first.")
    elif not topic.strip():
        st.warning("Please enter a topic or details first.")
    else:
        prompt = (
            f"Write a {tone.lower()} {content_type.lower()} about the following topic. "
            f"Keep the length {length.lower()}.\n\nTopic/Details: {topic}"
        )
        with st.spinner("Generating with Gemini..."):
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
        st.subheader("Generated Output")
        if success:
            st.markdown(result)
            st.download_button("📥 Download as .txt", result, file_name="generated_text.txt")
        else:
            st.error(result)
