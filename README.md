# Week 2 — Standalone Apps

Each file below is **fully independent** — run any one alone, no shared folder or `pages/` structure needed.

| File | Feature | API Used |
|---|---|---|
| `mini_project_chatbot.py` | **Mini Project**: AI Personal Assistant Chatbot (Chat Interface, AI Responses, Prompt Templates, Chat History, Streamlit UI) | OpenAI gpt-4o-mini |
| `prompt_playground.py` | Prompt Playground | OpenAI |
| `ai_text_generator.py` | AI Text Generator | Google Gemini (new SDK) |
| `ai_summarizer.py` | AI Summarizer | Google Gemini (new SDK) |
| `ai_translator.py` | AI Translator | OpenAI gpt-4o-mini |

## Setup (once)
```bash
pip install -r requirements.txt
```

## Run any one independently
```bash
streamlit run mini_project_chatbot.py
streamlit run prompt_playground.py
streamlit run ai_text_generator.py
streamlit run ai_summarizer.py
streamlit run ai_translator.py
```

Only one `streamlit run` command at a time normally uses port 8501 — if you want two running together, add `--server.port 8502` etc. to the second one.

## API Keys
Every file has its own sidebar key input(s) — nothing hardcoded, nothing saved to disk.
- OpenAI key: https://platform.openai.com/api-keys
- Gemini key: https://aistudio.google.com/apikey (free tier available)

## Note on Gemini SDK
Both `ai_text_generator.py` and `ai_summarizer.py` use the **new** SDK:
```python
from google import genai
client = genai.Client(api_key=...)
client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
```
Do not switch to `google.generativeai` — that's deprecated and 404s on this model naming.
