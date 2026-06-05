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

**Live demo:** https://machinelearningprojects-2hmpgrwojs9uresowepp3g.streamlit.app/

A deployable implementation of the **AI & Cybersecurity Integrated Assignment**:
a multi-agent + RAG student-support assistant with security engineered into the
request path. The app *is* the design — guardrails, RBAC, routing, and audit
logging all run live.

## What it does
- **Multi-agent + RAG (Part 1):** a Supervisor agent routes each question to one
  of **five specialist agents** — Course/FAQ, Troubleshoot, Placement, Career, and
  System & Security. Answers are grounded in a 44-entry knowledge base via retrieval.
  A live 5-stage pipeline and agent trace show the reasoning.
- **Security controls (Part 2):** input guardrail (blocks prompt injection),
  role-reactive RBAC matrix, output PII redaction, and an in-session SIEM-style audit log.
- **Diagrams & full design doc** in dedicated tabs.

## Tabs
1. **Assistant** — role-aware chat with a live routing → retrieval → generation pipeline.
2. **Architecture** — AI solution (5 agents) + three-tier network diagrams.
3. **Security** — live guardrail tester, role-reactive permission matrix, audit log.
4. **Design Doc** — the complete written assignment.

## Roles (RBAC)
Pick a role in the sidebar — Student, Staff, or Admin. Each role gets tailored
profile inputs, suggested questions, and a different effective-permissions matrix.

## LLM backend
Groq (primary) → Gemini (fallback) → **grounded mock** (no key needed).
To enable live generation, set a secret:

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
2. share.streamlit.io → New app → set `app.py` as the entry file.
3. (Optional) add `GROQ_API_KEY` under **Secrets**.

### HuggingFace Spaces
1. New Space → SDK **Streamlit**. 2. Upload all files. 3. (Optional) add keys under Settings → Secrets.

## Structure
```
app.py            # Streamlit dashboard (4 tabs)
theme.py          # design system: hero, pipeline, role badge, access matrix
agents.py         # supervisor router + 5 specialist agents (RAG + RBAC)
retriever.py      # TF-IDF RAG retriever (ChromaDB-ready interface)
llm.py            # Groq -> Gemini -> mock
guardrails.py     # input/output security controls
diagrams.py       # diagram asset paths
writeup.py        # full design document (Design Doc tab)
data/knowledge_base.py   # 44 grounded entries across 5 categories
assets_ai.png / assets_net.png
```
