# 🧠 Prompt Engineering & LLM APIs — Gen AI & ML Internship (Week 2)

Standalone Streamlit apps built as part of the **Gen AI & ML Internship** program, covering prompt engineering fundamentals and hands-on integration with the **OpenAI** and **Google Gemini** APIs.

Each app in this repo is **fully independent** — no shared files, no folder dependencies. Clone the repo, pick any file, and run it on its own.

---

## 🚀 Projects

| # | App | Description | API Used |
|---|-----|-------------|----------|
| 1 | **`mini_project_chatbot.py`** 🏆 | **Mini Project** — AI Personal Assistant Chatbot with chat interface, persona-based prompt templates, and full conversation history | OpenAI `gpt-4o-mini` |
| 2 | `prompt_playground.py` | Test and compare different system prompts + user prompts side by side | OpenAI |
| 3 | `ai_text_generator.py` | Generate blog posts, captions, emails, product descriptions & more | Google Gemini (new SDK) |
| 4 | `ai_summarizer.py` | Summarize long text into paragraphs, bullet points, or a one-line TL;DR | Google Gemini (new SDK) |
| 5 | `ai_translator.py` | Translate text between multiple languages | OpenAI `gpt-4o-mini` |

---

## 🏆 Mini Project — AI Personal Assistant Chatbot

The capstone deliverable for this week, built to spec:

- ✅ **Chat Interface** — `st.chat_message` + `st.chat_input`
- ✅ **AI Responses** — live calls to OpenAI's `gpt-4o-mini`
- ✅ **Prompt Templates** — 5 built-in personas (General Assistant, Senior Python Developer, Career Coach, Sarcastic Friend, Interview Prep Bot) + a Custom option
- ✅ **Chat History** — persisted across turns using `st.session_state`
- ✅ **Streamlit UI** — clean sidebar controls for persona, temperature, and API key

---

## 🛠️ Tech Stack

- **Frontend/UI:** Streamlit
- **LLM APIs:** OpenAI Python SDK, Google Gen AI SDK (`google-genai`)
- **Language:** Python 3.11

---

## ⚙️ Setup

```bash
# clone the repo
git clone https://github.com/pranab170/<repo-name>.git
cd <repo-name>

# (optional) create a virtual environment
conda create -n genai-week2 python=3.11 -y
conda activate genai-week2

# install dependencies
pip install -r requirements.txt
```

## ▶️ Run any app

```bash
streamlit run mini_project_chatbot.py
streamlit run prompt_playground.py
streamlit run ai_text_generator.py
streamlit run ai_summarizer.py
streamlit run ai_translator.py
```

Each app opens in your browser at `localhost:8501` by default. To run two apps side by side, add a different port to the second one:
```bash
streamlit run ai_text_generator.py --server.port 8502
```

---

## 🔑 API Keys

Every app has its own sidebar input for the key(s) it needs — **nothing is hardcoded, nothing is saved to disk.** Keys live only in `st.session_state` for the current browser session.

- Get an **OpenAI** key → https://platform.openai.com/api-keys
- Get a **Gemini** key (free tier available) → https://aistudio.google.com/apikey

---

## ⚠️ Important: Gemini SDK version

`ai_text_generator.py` and `ai_summarizer.py` use the **new** Google Gen AI SDK:

```python
from google import genai
client = genai.Client(api_key=...)
client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
```

Do **not** switch this to the deprecated `google.generativeai` package — it throws `404 NOT_FOUND` errors for `gemini-1.5-flash`-style model names on the current API surface.

---

## 📂 Repo Structure

```
.
├── mini_project_chatbot.py    # 🏆 Mini Project
├── prompt_playground.py
├── ai_text_generator.py
├── ai_summarizer.py
├── ai_translator.py
├── requirements.txt
└── README.md
```

---

## 👤 Author

**Pranab** — BTech CS (AI/ML), Centurion University of Technology and Management
GitHub: [@pranab170](https://github.com/pranab170)

---

*Built as part of the Gen AI & ML Internship — Week 2: Prompt Engineering & LLM APIs.*
