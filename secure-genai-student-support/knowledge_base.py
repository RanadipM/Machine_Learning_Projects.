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
    {
        "id": "course-ba",
        "category": "course",
        "title": "Business Analytics Program",
        "text": (
            "The Business Analytics program covers Excel, Power BI, Tableau, SQL, "
            "statistics for business, and case studies. Duration: 3 months. "
            "Suitable for commerce/MBA graduates and working professionals. "
            "No prior coding required."
        ),
    },
    {
        "id": "course-available",
        "category": "course",
        "title": "Available courses and programs",
        "text": (
            "The organization currently offers: Post Graduate Program in Data Science (PGPDS, 9 months), "
            "AI Engineering Track (4 months), Cybersecurity Fundamentals (8 weeks), "
            "and Business Analytics (3 months). Courses outside this list — such as "
            "Mechanical Engineering, Automobile Engineering, Civil Engineering, or other "
            "traditional engineering disciplines — are not offered. For the latest course "
            "catalogue contact staff or visit the website."
        ),
    },
    # ---- Fees & admission ----
    {
        "id": "course-fees",
        "category": "course",
        "title": "Fees, EMI and admission process",
        "text": (
            "Fees vary by program. PGPDS: payable in 3 installments, EMI available via "
            "partner banks. AI Engineering Track and Cybersecurity: one-time or 2-part "
            "payment. Admission requires an online application, a short aptitude test, "
            "and a counselling call. Scholarships are available for merit candidates. "
            "Contact admissions@organization.edu for exact fee amounts."
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
    {
        "id": "trouble-payment",
        "category": "troubleshoot",
        "title": "Payment and fee issues",
        "text": (
            "If a payment failed or is not reflecting: wait 30 minutes and check again. "
            "For net banking failures, the amount is auto-refunded in 5-7 business days. "
            "Share your transaction ID with accounts@organization.edu for faster resolution. "
            "Do not attempt the same payment twice without confirming with support first."
        ),
    },
    {
        "id": "trouble-certificate",
        "category": "troubleshoot",
        "title": "Certificate not received",
        "text": (
            "Certificates are issued within 2 weeks of course completion and final assessment. "
            "Check your registered email including spam/junk. If not received after 3 weeks, "
            "raise a ticket with your student ID and completion date. "
            "Digital certificates can be downloaded from the student portal under 'Achievements'."
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
        "title": "Typical roles and hiring partners",
        "text": (
            "Graduates are placed into Data Analyst, Junior Data Scientist, ML Engineer, "
            "AI Engineer, Business Analyst, and Cybersecurity Analyst roles. "
            "Hiring partners include analytics firms, fintech startups, IT services companies, "
            "and cybersecurity consultancies. Average time-to-placement is 2-4 months "
            "after eligibility."
        ),
    },
    {
        "id": "place-salary",
        "category": "placement",
        "title": "Salary ranges and package expectations",
        "text": (
            "Fresher packages typically range from 4-8 LPA for Data Analyst roles, "
            "6-12 LPA for Data Scientist / ML Engineer roles, and 8-15 LPA for AI Engineer roles "
            "depending on skills, portfolio quality, and company. "
            "Experienced professionals transitioning into data roles see higher packages. "
            "Salary depends on interview performance and individual skill demonstration."
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
    {
        "id": "career-cyber-path",
        "category": "career",
        "title": "Cybersecurity career path",
        "text": (
            "Entry roles: SOC Analyst, IT Security Analyst, Network Security Engineer. "
            "Progression: Security Engineer -> Security Architect -> CISO. "
            "Key certifications: CompTIA Security+, CEH, CISSP. "
            "Skills in demand: threat modeling, SIEM, penetration testing, cloud security. "
            "Strong growth sector with high demand across banking, IT, and government."
        ),
    },
    {
        "id": "career-switch",
        "category": "career",
        "title": "Career switching into data science or AI",
        "text": (
            "Students from non-CS backgrounds (engineering, commerce, science) successfully "
            "transition into data roles. Key steps: build Python/SQL fundamentals, "
            "complete a structured program like PGPDS, build 2-3 portfolio projects, "
            "and target analyst or junior roles first. "
            "Background in Mechanical, Civil, or other engineering can be an advantage "
            "in domain-specific data roles (manufacturing analytics, IoT, etc.)."
        ),
    },
    {
        "id": "career-fresher",
        "category": "career",
        "title": "Guidance for fresh graduates",
        "text": (
            "For fresh graduates: focus on one specialization (Data Science, AI, or Cybersecurity), "
            "build a GitHub portfolio with 3+ deployed projects, practice SQL and Python daily, "
            "and apply for internships alongside full-time roles. "
            "Certifications from Google, AWS, or Microsoft add credibility. "
            "Networking on LinkedIn and contributing to open-source projects helps visibility."
        ),
    },
    # ---- General / FAQ ----
    {
        "id": "faq-schedule",
        "category": "course",
        "title": "Class schedule and timing",
        "text": (
            "Live classes are held on weekends (Saturday and Sunday, 9am-1pm). "
            "Recorded sessions are available within 24 hours for those who miss live classes. "
            "Doubt-clearing sessions are held on weekday evenings (7-8pm). "
            "All timings are IST. International students can access recordings anytime."
        ),
    },
    {
        "id": "faq-refund",
        "category": "course",
        "title": "Refund and cancellation policy",
        "text": (
            "Full refund is available within 7 days of enrollment if no more than 2 classes "
            "have been attended. After 7 days, a pro-rata refund is issued based on "
            "remaining sessions. No refund after 50% course completion. "
            "Deferral to the next batch is available once at no extra charge."
        ),
    },
]
