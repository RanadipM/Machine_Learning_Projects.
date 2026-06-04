"""
Seed knowledge base for the RAG layer.
In production this would live in a vector DB (e.g. ChromaDB / pgvector).
Here it is an in-memory corpus with lightweight TF-IDF retrieval so the
demo runs anywhere with zero external services.
"""

KNOWLEDGE_BASE = [
    # ---- Courses ----
    {
        "id": "course-ds",
        "category": "course",
        "title": "Post Graduate Program in Data Science (PGPDS)",
        "text": (
            "The PGPDS is a 9-month program covering Python, SQL, statistics, "
            "machine learning, deep learning, and a capstone project. Eligibility: "
            "graduates in any quantitative discipline. Mode: hybrid (online + weekend "
            "labs). Fees are payable in 3 installments. EMI options are available."
        ),
    },
    {
        "id": "course-ai",
        "category": "course",
        "title": "AI Engineering Track",
        "text": (
            "The AI Engineering track covers LLMs, RAG pipelines, LangGraph multi-agent "
            "systems, vector databases, and deployment on HuggingFace and cloud. "
            "Prerequisite: working knowledge of Python. Duration: 4 months. Includes "
            "two graded projects and one portfolio capstone."
        ),
    },
    {
        "id": "course-cyber",
        "category": "course",
        "title": "Cybersecurity Fundamentals",
        "text": (
            "Cybersecurity Fundamentals covers network security, firewalls, TLS, access "
            "control, threat modeling, and monitoring/SIEM basics. No coding required. "
            "Duration: 8 weeks. Suitable for beginners and IT support staff."
        ),
    },
    # ---- Troubleshooting ----
    {
        "id": "trouble-login",
        "category": "troubleshoot",
        "title": "Login and password issues",
        "text": (
            "If you cannot log in: (1) use 'Forgot password' to reset, (2) ensure your "
            "MFA app time is synced, (3) clear browser cache. Accounts lock after 5 "
            "failed attempts and auto-unlock in 15 minutes. Contact staff if locked out "
            "repeatedly."
        ),
    },
    {
        "id": "trouble-video",
        "category": "troubleshoot",
        "title": "Video / lab environment not loading",
        "text": (
            "If lecture videos or the lab environment do not load: check your internet, "
            "try an incognito window, disable ad-blockers, and ensure the browser is "
            "updated. Lab environments require WebSockets to be allowed. If the issue "
            "persists, raise a ticket and a support engineer will respond within 24 hours."
        ),
    },
    # ---- Placements ----
    {
        "id": "place-process",
        "category": "placement",
        "title": "Placement process and eligibility",
        "text": (
            "Placement support begins after 70% course completion and a passing capstone. "
            "Students get resume reviews, mock interviews, and access to the employer "
            "portal. Eligibility for the guaranteed-interview pool requires 85%+ "
            "attendance and at least one deployed portfolio project."
        ),
    },
    {
        "id": "place-roles",
        "category": "placement",
        "title": "Typical roles and partners",
        "text": (
            "Graduates are placed into Data Analyst, Junior Data Scientist, ML Engineer, "
            "and AI Engineer roles. Hiring partners include analytics firms, fintech "
            "startups, and IT services companies. Average time-to-placement is 2-4 months "
            "after eligibility."
        ),
    },
    # ---- Career guidance ----
    {
        "id": "career-ds-path",
        "category": "career",
        "title": "Data Science career path",
        "text": (
            "A typical path: Data Analyst (SQL, dashboards) -> Junior Data Scientist "
            "(ML modeling, statistics) -> Data Scientist / ML Engineer (production ML, "
            "MLOps). Building a strong portfolio with deployed projects accelerates this. "
            "Quantitative finance and AI engineering are popular specializations."
        ),
    },
    {
        "id": "career-ai-path",
        "category": "career",
        "title": "AI Engineer career path",
        "text": (
            "AI Engineers focus on LLM applications, RAG, agentic systems, and "
            "deployment. Recommended skills: Python, LangChain/LangGraph, vector "
            "databases, prompt engineering, evaluation (RAGAS), and cloud deployment. "
            "A public portfolio of deployed AI apps strongly improves hiring outcomes."
        ),
    },
]
