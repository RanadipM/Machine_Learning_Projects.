---
title: Secure GenAI Student Support
emoji: 🎓
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.36.0
app_file: app.py
pinned: false
---

# Secure GenAI Student-Support Assistant

A deployable implementation of the **AI & Cybersecurity Integrated Assignment**:
a multi-agent + RAG student-support assistant with security guardrails baked in.

## What it does
- **Multi-agent + RAG (Part 1):** a Supervisor agent routes each question to a
  specialised agent (Course/FAQ, Troubleshoot, Placement, Career). Answers are
  grounded in a knowledge base via retrieval. The agent trace is shown live.
- **Security controls (Part 2):** input guardrail (blocks prompt injection),
  RBAC roles, output PII redaction, and an in-session audit log (SIEM-style).
- **Diagrams & full design doc** in dedicated tabs.

## Tabs
1. **Assistant** — live chat with visible routing → retrieval → generation trace.
2. **Architecture** — AI solution and three-tier network diagrams.
3. **Security** — test the guardrail, view RBAC, watch the audit log populate.
4. **Design Doc** — the complete written assignment.

## LLM backend
Groq (primary) → Gemini (fallback) → **grounded mock** (no key needed).
The app runs out of the box in mock mode. To enable live generation, set a secret:

```
GROQ_API_KEY = "..."
# or
GEMINI_API_KEY = "..."
```

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

### Streamlit Community Cloud
1. Push this folder to a GitHub repo.
2. On share.streamlit.io → New app → pick the repo, set `app.py` as the entry file.
3. (Optional) Add `GROQ_API_KEY` / `GEMINI_API_KEY` under **Secrets**.

### HuggingFace Spaces
1. Create a new Space → SDK: **Streamlit**.
2. Upload all files (the YAML header in this README configures the Space).
3. (Optional) Add keys under **Settings → Variables and secrets**.

## Structure
```
app.py            # Streamlit UI (4 tabs)
agents.py         # supervisor router + specialised agents (RAG + RBAC)
retriever.py      # TF-IDF RAG retriever (swap for ChromaDB in prod)
llm.py            # Groq -> Gemini -> mock
guardrails.py     # input/output security controls
diagrams.py       # diagram asset paths
writeup.py        # full design document
data/knowledge_base.py
assets_ai.png / assets_net.png
```
