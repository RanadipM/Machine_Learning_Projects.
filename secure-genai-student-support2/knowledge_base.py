"""
Comprehensive knowledge base for a mid-sized training organization.
Covers ALL query types from the assignment brief:
  - Courses / programs (eligibility, fees, schedule, curriculum)
  - Troubleshooting (login, platform, payment, certificates)
  - Placements (process, roles, salary, employers)
  - Career guidance (paths, switching, fresher tips, skills)

In production this lives in ChromaDB / pgvector.
Here: in-memory TF-IDF RAG — zero external dependencies.
"""

KNOWLEDGE_BASE = [

    # ══════════════════════════════════════════════════════
    # SECTION 1 — COURSES & PROGRAMS
    # ══════════════════════════════════════════════════════

    {
        "id": "course-overview",
        "category": "course",
        "title": "All courses offered by the organization",
        "text": (
            "The organization offers four programs: "
            "(1) Post Graduate Program in Data Science (PGPDS) — 9 months, "
            "(2) AI Engineering Track — 4 months, "
            "(3) Cybersecurity Fundamentals — 8 weeks, "
            "(4) Business Analytics Program — 3 months. "
            "Courses outside this list — such as Automobile Engineering, Mechanical, "
            "Civil, Medical, or Law — are NOT offered. "
            "For the latest catalogue contact admissions or visit the website."
        ),
    },
    {
        "id": "course-pgpds",
        "category": "course",
        "title": "Post Graduate Program in Data Science (PGPDS) — full details",
        "text": (
            "PGPDS is the flagship 9-month hybrid program. "
            "Curriculum: Python, SQL, statistics, probability, machine learning, "
            "deep learning, NLP, time-series analysis, and a capstone project. "
            "Eligibility: bachelor's degree in any stream (science, commerce, engineering). "
            "No prior coding required — Python is taught from scratch. "
            "Mode: weekend live classes (Sat–Sun 9 am–1 pm IST) + weekday recordings. "
            "Batch size: 40–50 students. Mentorship and doubt sessions included."
        ),
    },
    {
        "id": "course-ai",
        "category": "course",
        "title": "AI Engineering Track — full details",
        "text": (
            "The AI Engineering Track is a 4-month advanced program. "
            "Curriculum: Large Language Models (LLMs), prompt engineering, "
            "RAG pipelines, LangChain and LangGraph, multi-agent systems, "
            "vector databases (ChromaDB, pgvector), model evaluation (RAGAS), "
            "and cloud deployment on HuggingFace Spaces and AWS. "
            "Prerequisite: Python proficiency (at least 3 months experience). "
            "Includes two graded projects and one portfolio capstone. "
            "Suitable for working professionals and PGPDS graduates."
        ),
    },
    {
        "id": "course-cyber",
        "category": "course",
        "title": "Cybersecurity Fundamentals — full details",
        "text": (
            "Cybersecurity Fundamentals is an 8-week evening program. "
            "Curriculum: network security, OSI model, firewalls, TLS/HTTPS, "
            "access control and RBAC, threat modeling, OWASP Top 10, "
            "SIEM and log monitoring, incident response basics. "
            "No coding required — suitable for IT staff, analysts, and managers. "
            "Classes: Monday, Wednesday, Friday evenings 7–9 pm IST. "
            "Certification exam preparation included (CompTIA Security+ aligned)."
        ),
    },
    {
        "id": "course-ba",
        "category": "course",
        "title": "Business Analytics Program — full details",
        "text": (
            "Business Analytics is a 3-month weekend program. "
            "Curriculum: Excel advanced, Power BI, Tableau, SQL for business, "
            "statistics for decision-making, and business case studies. "
            "No prior coding required. Suitable for commerce/MBA graduates, "
            "finance professionals, and working managers. "
            "Includes a live industry project using a real dataset."
        ),
    },
    {
        "id": "course-eligibility",
        "category": "course",
        "title": "Eligibility criteria for all programs",
        "text": (
            "PGPDS: any bachelor's degree, no coding required, minimum 50% aggregate. "
            "AI Engineering: bachelor's degree + Python proficiency (tested at admission). "
            "Cybersecurity: any graduate or working professional, no coding required. "
            "Business Analytics: any graduate, especially commerce/MBA backgrounds. "
            "Working professionals and career-switchers are actively encouraged to apply. "
            "Age: no upper limit. Freshers and experienced candidates both eligible."
        ),
    },
    {
        "id": "course-fees",
        "category": "course",
        "title": "Course fees, EMI, and payment options",
        "text": (
            "PGPDS: INR 1,20,000 total — payable in 3 installments of INR 40,000. "
            "AI Engineering Track: INR 60,000 — payable in 2 installments. "
            "Cybersecurity Fundamentals: INR 25,000 — one-time or 2-part payment. "
            "Business Analytics: INR 35,000 — one-time or 2-part payment. "
            "EMI available via partner banks (0% EMI for 6 months for PGPDS). "
            "Scholarships: merit-based 10–25% discount available. "
            "Corporate sponsorship letters accepted. GST applicable at 18%. "
            "Contact fees@organization.edu for exact quotes and scholarship eligibility."
        ),
    },
    {
        "id": "course-schedule",
        "category": "course",
        "title": "Class schedule, timings, and batch dates",
        "text": (
            "Live classes: weekends — Saturday and Sunday 9 am–1 pm IST. "
            "Cybersecurity evening batch: Mon/Wed/Fri 7–9 pm IST. "
            "Recordings uploaded within 24 hours for those who miss sessions. "
            "Doubt sessions: weekday evenings 7–8 pm IST (separate Zoom link). "
            "New batches start every 2 months — January, March, May, July, September, November. "
            "Exact batch dates announced 3 weeks before start. "
            "International students: all content accessible asynchronously with live Q&A support."
        ),
    },
    {
        "id": "course-admission",
        "category": "course",
        "title": "Admission process and how to apply",
        "text": (
            "Step 1: Fill the online application form at organization website. "
            "Step 2: Appear for a short aptitude assessment (30 minutes, online). "
            "Step 3: Attend a counselling call with an admission advisor (15 minutes). "
            "Step 4: Pay the registration fee (INR 2,000, adjustable against course fee). "
            "Step 5: Receive offer letter and access credentials within 48 hours. "
            "AI Engineering Track requires an additional Python proficiency test. "
            "Applications close 1 week before batch start. Apply early — seats are limited to 40–50 per batch."
        ),
    },
    {
        "id": "course-refund",
        "category": "course",
        "title": "Refund policy and course deferral",
        "text": (
            "Full refund (100%): within 7 days of enrollment if fewer than 2 sessions attended. "
            "Partial refund (50%): 8–14 days after enrollment. "
            "No refund after 14 days or after 50% course completion. "
            "Deferral: allowed once per student at no extra charge — move to the next batch. "
            "Request deferral at least 7 days before batch starts. "
            "Refund processed within 7–10 business days to original payment method. "
            "Contact refunds@organization.edu with your enrollment ID for all refund requests."
        ),
    },
    {
        "id": "course-curriculum-compare",
        "category": "course",
        "title": "How to choose between courses — comparison guide",
        "text": (
            "Choose PGPDS if: you are a fresher or career-switcher wanting a comprehensive "
            "foundation in data science with placement support. "
            "Choose AI Engineering if: you already know Python and want to specialize in "
            "LLMs, RAG, and agentic AI systems for AI Engineer / ML Engineer roles. "
            "Choose Cybersecurity if: you work in IT or want to move into security roles, "
            "no coding background needed. "
            "Choose Business Analytics if: you are in a business/finance role and want to "
            "use data tools (Power BI, Tableau) without learning to code. "
            "Unsure? Book a free counselling call — advisors will recommend the best fit."
        ),
    },

    # ══════════════════════════════════════════════════════
    # SECTION 2 — TROUBLESHOOTING / PLATFORM ISSUES
    # ══════════════════════════════════════════════════════

    {
        "id": "trouble-login",
        "category": "troubleshoot",
        "title": "Cannot log in / account locked",
        "text": (
            "If you cannot log in: "
            "(1) Click 'Forgot password' on the login page and reset via your registered email. "
            "(2) Check your MFA/authenticator app — ensure phone time is synced. "
            "(3) Clear browser cache and cookies, then try again. "
            "(4) Try an incognito/private window to rule out browser extensions. "
            "Accounts lock automatically after 5 failed login attempts and auto-unlock in 15 minutes. "
            "If still locked after 15 minutes, contact support@organization.edu with your Student ID."
        ),
    },
    {
        "id": "trouble-password",
        "category": "troubleshoot",
        "title": "Password reset and MFA issues",
        "text": (
            "To reset password: go to login page → 'Forgot password' → enter registered email → "
            "check inbox (including spam/junk) for reset link — link valid for 30 minutes. "
            "MFA not working: ensure your phone clock is correct (Settings → Date & Time → Auto). "
            "Lost MFA device: email support@organization.edu with Student ID and a government ID — "
            "MFA reset within 24 hours after identity verification. "
            "First-time login: use the credentials in your welcome email — change password on first login."
        ),
    },
    {
        "id": "trouble-video",
        "category": "troubleshoot",
        "title": "Videos / lectures not loading or buffering",
        "text": (
            "If videos are not loading or buffering: "
            "(1) Check your internet speed — minimum 5 Mbps required for HD video. "
            "(2) Try Chrome or Firefox — Safari may have compatibility issues. "
            "(3) Disable VPN if active — some VPNs block our CDN. "
            "(4) Disable browser extensions, especially ad-blockers. "
            "(5) Try an incognito window. "
            "(6) If using mobile, switch to the mobile app instead of browser. "
            "Recordings are on a CDN — if still slow, change video quality to 480p. "
            "If issue persists for over 24 hours, raise a ticket with your browser version and ISP name."
        ),
    },
    {
        "id": "trouble-lab",
        "category": "troubleshoot",
        "title": "Lab environment / coding sandbox not working",
        "text": (
            "Lab environments require WebSockets — make sure your firewall or corporate proxy "
            "does not block WebSocket connections (ws:// and wss://). "
            "Supported browsers: Chrome 90+, Firefox 88+, Edge 90+. "
            "If the lab shows a blank screen: hard-refresh (Ctrl+Shift+R / Cmd+Shift+R). "
            "If the kernel keeps disconnecting: your session may have timed out — click 'Reconnect'. "
            "For persistent issues raise a ticket with your Student ID, browser version, "
            "and a screenshot — support engineers respond within 24 hours."
        ),
    },
    {
        "id": "trouble-zoom",
        "category": "troubleshoot",
        "title": "Live class / Zoom link not working",
        "text": (
            "Live class links are emailed 1 hour before each session and also posted in the "
            "student portal under 'Upcoming Classes'. "
            "If the link does not work: (1) Check you are using the latest Zoom version. "
            "(2) Try joining via browser (zoom.us/join) instead of the app. "
            "(3) Check the email for the correct meeting ID and passcode. "
            "If you are more than 10 minutes late, the host may have locked the room — "
            "message the class WhatsApp group for the waiting room to be opened. "
            "Missed a live class? Recordings are up within 24 hours on the portal."
        ),
    },
    {
        "id": "trouble-payment",
        "category": "troubleshoot",
        "title": "Payment failed or not reflecting",
        "text": (
            "If your payment failed: wait 30 minutes before retrying — double payment "
            "may cause billing issues. Check your bank statement first. "
            "If money was debited but portal shows unpaid: share your transaction ID / "
            "UTR number with fees@organization.edu — resolved within 2 business days. "
            "Net banking failures: amount is auto-refunded in 5–7 business days. "
            "UPI issues: screenshot the UPI success message and email it to fees@. "
            "Do not attempt the same payment twice without confirming with support. "
            "GST invoice is emailed within 24 hours of successful payment."
        ),
    },
    {
        "id": "trouble-certificate",
        "category": "troubleshoot",
        "title": "Certificate not received / download issues",
        "text": (
            "Certificates are issued within 14 days of course completion and final assessment. "
            "Check your registered email including spam/junk folders. "
            "Download from portal: Student Dashboard → Achievements → Download Certificate. "
            "If not available after 21 days: raise a ticket with your Student ID and "
            "completion date — team will investigate within 3 business days. "
            "LinkedIn certificate: use the 'Add to LinkedIn' button in the portal for "
            "automatic verification. Credential ID is printed on each certificate. "
            "Hard-copy certificates available on request (courier charges apply)."
        ),
    },
    {
        "id": "trouble-content",
        "category": "troubleshoot",
        "title": "Course content missing or access denied",
        "text": (
            "If content is locked: check whether you have paid the current installment — "
            "content unlocks in tiers after each payment. "
            "If payment is complete but content is still locked: log out, clear cache, log back in. "
            "Waitlist for an upcoming module: some advanced modules unlock week-by-week as per "
            "the curriculum schedule — this is expected. "
            "Wrong course showing: contact support with your enrollment ID to verify your "
            "registered course. "
            "Content error (incorrect information, broken link): report via the 'Report Issue' "
            "button on each lesson page — reviewed within 48 hours."
        ),
    },
    {
        "id": "trouble-general",
        "category": "troubleshoot",
        "title": "How to raise a support ticket",
        "text": (
            "For any unresolved issue: "
            "Email support@organization.edu with Subject: [Student ID] — Issue Summary. "
            "Or use the Help button in the student portal (bottom-right corner). "
            "Response time: within 24 hours on weekdays, 48 hours on weekends. "
            "For urgent issues (exam day, live class, payment): call the helpdesk at "
            "+91-XXXXXXXXXX (9 am–8 pm IST, Mon–Sat). "
            "Always include your Student ID, course name, and a screenshot if possible — "
            "this speeds up resolution significantly."
        ),
    },

    # ══════════════════════════════════════════════════════
    # SECTION 3 — PLACEMENTS
    # ══════════════════════════════════════════════════════

    {
        "id": "place-overview",
        "category": "placement",
        "title": "Placement support — what is provided",
        "text": (
            "The organization provides end-to-end placement support including: "
            "resume building and review, LinkedIn profile optimization, "
            "mock technical interviews (2 rounds per student), "
            "aptitude and HR interview coaching, "
            "access to the employer portal with live job listings, "
            "and referrals to hiring partners. "
            "Placement support is available for 12 months after course completion. "
            "A dedicated placement coordinator is assigned per batch."
        ),
    },
    {
        "id": "place-eligibility",
        "category": "placement",
        "title": "Placement eligibility criteria",
        "text": (
            "To be eligible for placement support and the guaranteed-interview pool: "
            "(1) Complete at least 70% of the course. "
            "(2) Pass the capstone project with a score of 60% or above. "
            "(3) Maintain 85%+ attendance in live sessions. "
            "(4) Have at least one deployed portfolio project (GitHub + live demo link). "
            "Students who do not meet all criteria still receive resume and portal access "
            "but are not in the guaranteed-interview pool. "
            "Catch-up sessions available for students with low attendance due to medical reasons."
        ),
    },
    {
        "id": "place-process",
        "category": "placement",
        "title": "How the placement process works — step by step",
        "text": (
            "Step 1: After 70% course completion, register on the Placement Portal. "
            "Step 2: Submit your resume for review — 2 revision rounds included. "
            "Step 3: Complete the placement readiness assessment (aptitude + coding/SQL). "
            "Step 4: Attend 2 mock interview rounds with industry mentors — feedback provided. "
            "Step 5: Shortlisted profiles are shared with hiring partners every 2 weeks. "
            "Step 6: Attend interviews — portal tracks all applications and status. "
            "Step 7: Offer letter received — placement team assists with negotiation. "
            "Average time from placement registration to first offer: 2–4 months."
        ),
    },
    {
        "id": "place-roles",
        "category": "placement",
        "title": "Job roles and companies that hire from us",
        "text": (
            "Roles our graduates get hired into: "
            "Data Analyst, Junior Data Scientist, ML Engineer, AI Engineer, "
            "Business Analyst, Data Engineer, Cybersecurity Analyst, SOC Analyst. "
            "Hiring partners include: analytics consulting firms, fintech startups, "
            "e-commerce companies, IT services giants (Infosys, TCS, Wipro, Accenture), "
            "banking and insurance firms, and product companies. "
            "PGPDS graduates primarily get Data Analyst and Junior Data Scientist roles. "
            "AI Engineering graduates target AI Engineer, ML Engineer, and LLM Engineer roles. "
            "Cybersecurity graduates target SOC Analyst and Security Engineer roles."
        ),
    },
    {
        "id": "place-salary",
        "category": "placement",
        "title": "Expected salary / CTC packages",
        "text": (
            "Fresher salary ranges (indicative, varies by company and city): "
            "Data Analyst: INR 4–7 LPA. "
            "Junior Data Scientist: INR 6–10 LPA. "
            "ML / AI Engineer: INR 8–15 LPA. "
            "Business Analyst: INR 4–8 LPA. "
            "Cybersecurity Analyst: INR 5–9 LPA. "
            "Career-switchers with prior work experience typically get 30–50% higher packages. "
            "Salaries depend on portfolio quality, interview performance, and city. "
            "Mumbai, Bengaluru, Hyderabad, and Pune offer the highest packages."
        ),
    },
    {
        "id": "place-portfolio",
        "category": "placement",
        "title": "Building a strong portfolio for placement",
        "text": (
            "A strong portfolio significantly increases placement chances. Recommended projects: "
            "1. End-to-end ML project deployed on Streamlit or Gradio (e.g., credit risk predictor). "
            "2. EDA and Power BI / Tableau dashboard on a real dataset. "
            "3. NLP project (sentiment analysis, text classification). "
            "4. For AI Engineering: a RAG pipeline or multi-agent chatbot deployed on HuggingFace. "
            "5. For Cybersecurity: a network scan or SIEM log analysis write-up. "
            "All projects must be on GitHub with a README, requirements.txt, and live demo link. "
            "Placement team reviews your portfolio before forwarding to companies."
        ),
    },
    {
        "id": "place-internship",
        "category": "placement",
        "title": "Internship opportunities",
        "text": (
            "The organization facilitates internship opportunities for students in the final "
            "2 months of their course. Internships available in: "
            "data analysis, ML model building, business intelligence, and cybersecurity. "
            "Duration: 2–3 months, stipend INR 5,000–15,000 per month (varies by company). "
            "Some internships convert to full-time roles. "
            "Eligibility: 60%+ attendance and capstone project submitted. "
            "Register interest with the placement coordinator by the 5th month of PGPDS."
        ),
    },

    # ══════════════════════════════════════════════════════
    # SECTION 4 — CAREER GUIDANCE
    # ══════════════════════════════════════════════════════

    {
        "id": "career-ds-path",
        "category": "career",
        "title": "Data Science career path and progression",
        "text": (
            "Typical Data Science career progression: "
            "Data Analyst (0–2 years) → Junior Data Scientist (2–4 years) → "
            "Data Scientist (4–6 years) → Senior Data Scientist / ML Engineer → "
            "Lead / Principal Data Scientist → Head of Data / Chief Data Officer. "
            "Key skills at each stage: "
            "Analyst: SQL, Excel, Power BI, basic Python. "
            "Junior DS: ML algorithms, scikit-learn, statistics, feature engineering. "
            "Data Scientist: model deployment, MLOps, experiment design, A/B testing. "
            "Senior: architecture, mentoring, business strategy, cloud platforms (AWS/GCP/Azure)."
        ),
    },
    {
        "id": "career-ai-path",
        "category": "career",
        "title": "AI Engineering career path",
        "text": (
            "AI Engineering career progression: "
            "Junior AI Engineer → AI Engineer → Senior AI Engineer → "
            "AI Architect → Principal AI Engineer / Head of AI. "
            "Core skills: Python, LLM APIs (OpenAI, Groq, Gemini), LangChain/LangGraph, "
            "RAG pipelines, vector databases, prompt engineering, RAGAS evaluation, "
            "cloud deployment (AWS Lambda, HuggingFace, Azure AI). "
            "Differentiators: deployed portfolio, open-source contributions, "
            "knowledge of MLOps (MLflow, W&B), and system design for AI products. "
            "High-demand sector — roles growing 40%+ YoY in India and globally."
        ),
    },
    {
        "id": "career-cyber-path",
        "category": "career",
        "title": "Cybersecurity career path",
        "text": (
            "Cybersecurity career progression: "
            "SOC Analyst (Tier 1) → SOC Analyst (Tier 2/3) → Security Engineer → "
            "Security Architect → CISO / VP of Security. "
            "Specializations: Application Security, Cloud Security, Penetration Testing, "
            "GRC (Governance Risk Compliance), Digital Forensics. "
            "Key certifications: CompTIA Security+ (entry), CEH (mid), CISSP (senior). "
            "High-growth sector especially in BFSI, IT services, government, and healthcare. "
            "Starting salary: 5–9 LPA for freshers; 15–30 LPA for certified senior professionals."
        ),
    },
    {
        "id": "career-ba-path",
        "category": "career",
        "title": "Business Analytics career path",
        "text": (
            "Business Analytics career progression: "
            "Business Analyst → Senior BA → Analytics Manager → "
            "Director of Analytics / VP Business Intelligence. "
            "Key tools: SQL, Excel, Power BI, Tableau, Python (basic). "
            "Industries hiring heavily: FMCG, retail, banking, telecom, consulting. "
            "For MBA graduates transitioning to analytics: "
            "start as a Business Analyst or Strategy Analyst at a consulting firm — "
            "domain expertise (finance, marketing) combined with data skills is very valued. "
            "Average starting package: 5–9 LPA with strong upside for experienced professionals."
        ),
    },
    {
        "id": "career-switch",
        "category": "career",
        "title": "Career switching into data science from non-IT backgrounds",
        "text": (
            "Career switching is very common and successful. Advice for backgrounds: "
            "Mechanical/Civil/Electrical Engineering: target manufacturing analytics, "
            "IoT data, or supply-chain analytics — domain knowledge is a real advantage. "
            "Commerce/MBA/Finance: target fintech, risk analytics, or business intelligence — "
            "your business understanding sets you apart from pure CS graduates. "
            "Science (Physics/Chemistry/Biology): target research analytics, "
            "pharma data science, or clinical trial analytics. "
            "Teaching/Education: target ed-tech analytics or learning & development data roles. "
            "Key advice: build 2–3 domain-specific projects, not generic Titanic/Iris datasets. "
            "Switchers with 2+ years of prior experience often get 6–10 LPA as first data role."
        ),
    },
    {
        "id": "career-fresher",
        "category": "career",
        "title": "Tips for fresh graduates entering data science / AI",
        "text": (
            "For fresh graduates starting their data career: "
            "1. Focus: pick one track (Data Science, AI Engineering, or Cybersecurity) and go deep. "
            "2. Portfolio: build 3+ projects on GitHub with live demos — quality over quantity. "
            "3. Skills: master SQL and Python first — they appear in 90% of job descriptions. "
            "4. Certifications: Google Data Analytics, AWS Cloud Practitioner, or Azure AI Fundamentals "
            "add credibility at fresher level. "
            "5. Network: update LinkedIn weekly, connect with recruiters, and engage with content. "
            "6. Apply early: start applying in the 5th month of PGPDS — don't wait for completion. "
            "7. Mock interviews: practice LeetCode (Easy/Medium SQL) and case studies weekly."
        ),
    },
    {
        "id": "career-skills",
        "category": "career",
        "title": "Most in-demand skills for data and AI jobs in 2025–26",
        "text": (
            "Top skills employers look for right now: "
            "Data Science: Python, SQL, scikit-learn, statistical thinking, Power BI/Tableau, "
            "ML model deployment, MLOps basics, communication skills. "
            "AI Engineering: LLM APIs, RAG architecture, LangChain/LangGraph, vector databases, "
            "prompt engineering, Python, cloud deployment, RAGAS evaluation. "
            "Cybersecurity: network fundamentals, SIEM tools (Splunk, ELK), Python scripting, "
            "cloud security (AWS/Azure), incident response, threat intelligence. "
            "Business Analytics: SQL, Excel, Power BI, storytelling with data, "
            "business acumen, stakeholder communication. "
            "Soft skills important across all: problem-solving, communication, teamwork, "
            "and the ability to explain technical concepts to non-technical stakeholders."
        ),
    },
    {
        "id": "career-mentor",
        "category": "career",
        "title": "Mentorship and career counselling available",
        "text": (
            "The organization provides: "
            "1. One-on-one career counselling sessions (2 per student) with industry mentors. "
            "2. Monthly alumni talks from graduates working at top companies. "
            "3. LinkedIn profile review by placement coordinators. "
            "4. Resume review with ATS (Applicant Tracking System) optimization. "
            "5. Study groups and peer learning pods organized by batch. "
            "Book a career counselling session via the portal under 'Career Support'. "
            "Alumni mentors are available for informal chats via the alumni network portal. "
            "Career counsellors can guide you on which role to target given your background."
        ),
    },
    {
        "id": "career-higher-studies",
        "category": "career",
        "title": "Higher studies — MS, MBA, PhD after this program",
        "text": (
            "The organization's programs complement higher studies applications: "
            "MS in Data Science / AI (USA, Canada, UK, Germany): "
            "PGPDS + strong projects strengthens GRE/IELTS applications. "
            "MBA with Data/Analytics specialization: "
            "Business Analytics program is directly useful for CAT/GMAT prep alongside work. "
            "PhD in CS / AI (India — IIT, IIIT, IISc, IISER): "
            "AI Engineering Track portfolio and research projects improve PhD applications. "
            "Some graduates use the PGPDS capstone as a foundation for a research paper. "
            "For PhD guidance, speak to the academic mentorship team via the portal."
        ),
    },

    # ══════════════════════════════════════════════════════
    # SECTION 5 — GENERAL FAQ
    # ══════════════════════════════════════════════════════

    {
        "id": "faq-contact",
        "category": "course",
        "title": "Contact details and support channels",
        "text": (
            "General enquiries: info@organization.edu "
            "Admissions: admissions@organization.edu "
            "Fees and payments: fees@organization.edu "
            "Technical support: support@organization.edu "
            "Placement team: placement@organization.edu "
            "Refunds: refunds@organization.edu "
            "Phone helpdesk: +91-XXXXXXXXXX (Mon–Sat, 9 am–8 pm IST). "
            "Student portal: portal.organization.edu "
            "Response time: email within 24 hours on weekdays, 48 hours on weekends."
        ),
    },
    {
        "id": "faq-community",
        "category": "course",
        "title": "Student community, WhatsApp groups, and alumni network",
        "text": (
            "Every batch has a dedicated WhatsApp group — link shared in the welcome email. "
            "Student Discord server: channels for each course, doubt-clearing, job postings, "
            "project collaboration, and off-topic socializing. "
            "Alumni network: 2,000+ alumni across India and abroad — accessible via the portal. "
            "Alumni mentoring: opt-in program where senior alumni provide 1-on-1 guidance. "
            "Hackathons: inter-batch hackathons held every quarter — prizes and certificates awarded. "
            "Guest lectures: monthly sessions by industry experts from top companies."
        ),
    },

    # ══════════════════════════════════════════════════════
    # SECTION 6 — SYSTEM SECURITY & ADMIN (Part 2 of assignment)
    # ══════════════════════════════════════════════════════

    {
        "id": "sys-monitoring",
        "category": "system",
        "title": "What the system monitors — logs and events",
        "text": (
            "The platform tracks: authentication events (login success/failure, MFA, "
            "password resets, account lockouts), API usage (endpoint, caller, status code, "
            "latency, rate-limit hits), data-access events (who read/wrote which student or "
            "employer record), AI/agent events (queries, retrieved sources, guardrail triggers, "
            "token/cost usage), and infrastructure events (firewall denies, config changes, "
            "admin actions). All logs flow into a SIEM with alerting thresholds for anomaly "
            "detection — spikes in failed logins, abnormal API volume, or access from new "
            "geographies trigger alerts to the on-call team."
        ),
    },
    {
        "id": "sys-rbac",
        "category": "system",
        "title": "Access control — RBAC across Admin, Staff, Student",
        "text": (
            "The platform uses least-privilege Role-Based Access Control (RBAC), enforced "
            "server-side on every request. Admin: manage users, configs, infrastructure, and "
            "view audit logs (cannot bypass MFA; all actions logged). Staff: view and manage "
            "assigned students, placements, and content (cannot change system config or see "
            "other staff's restricted data). Student: use the assistant and view their own "
            "profile, courses, and placement data (cannot access other students' data or admin "
            "functions). Authentication uses strong passwords plus MFA for Admin and Staff, "
            "with session timeouts and brute-force lockout."
        ),
    },
    {
        "id": "sys-dataprotection",
        "category": "system",
        "title": "How student data is protected",
        "text": (
            "Student data is protected by defense-in-depth: encryption at rest (AES-256 for "
            "the database, passwords hashed with bcrypt/Argon2) and in transit (TLS 1.2+/1.3 "
            "everywhere, including internal service calls). Data minimization ensures only the "
            "data needed for an answer reaches the AI model, and PII is masked or tokenized. "
            "Output guardrails redact emails, phone numbers, and long ID numbers before any "
            "response leaves the system. Network segmentation keeps the database in an isolated "
            "subnet with no internet route. Logs mask PII, and periodic privacy reviews and "
            "red-teaming confirm there are no leakage paths."
        ),
    },
    {
        "id": "sys-secrets",
        "category": "system",
        "title": "How API keys and secrets are managed",
        "text": (
            "API keys and secrets are never stored in code or repositories. They live in a "
            "secrets manager / vault with automatic rotation and least-privilege scoping. "
            "If a key is leaked: immediate actions are to revoke and rotate the key, invalidate "
            "derived sessions, inspect logs for unauthorized use and unusual spend, and block "
            "suspicious sources. Long-term hardening includes short-lived auto-rotated keys, "
            "CI secret-scanning, pre-commit hooks, spend and rate alerts, and a root-cause "
            "review to close the gap that caused the leak."
        ),
    },
    {
        "id": "sys-ai-safety",
        "category": "system",
        "title": "What happens if the AI gives incorrect information",
        "text": (
            "Incorrect AI output is detected through user feedback (thumbs up/down, reports), "
            "scheduled automated evaluation against a curated golden Q&A set, guardrail and "
            "hallucination flags, and staff spot-checks of a sample of conversations. To fix it: "
            "reproduce the failing cases, then address the root cause — improve or expand the "
            "RAG knowledge base, tighten prompts and guardrails, add validation rules, or roll "
            "back to a known-good model/prompt version. Each fix is re-tested on the eval set "
            "before redeploying, and the failure cases are added to a regression suite so the "
            "issue cannot silently recur. RAG grounding ensures answers come from the knowledge "
            "base rather than the model inventing facts."
        ),
    },
    {
        "id": "sys-risks",
        "category": "system",
        "title": "Security risks and how they are mitigated",
        "text": (
            "Key risks and mitigations: API misuse / DDoS — WAF, per-key rate limits and quotas, "
            "autoscaling with cost ceilings, and a CDN. Unauthorized access — least-privilege "
            "RBAC, MFA, short-lived tokens, and network segmentation so the database is "
            "unreachable from outside. Data leakage — PII masking in logs, output redaction, "
            "encryption at rest, and strict response field-filtering. Phishing / credential "
            "theft — MFA so a stolen password alone is useless, plus awareness training and "
            "anomaly detection. Prompt injection (AI-specific) — input guardrails, separating "
            "instructions from user content, scoped tool permissions, and output validation."
        ),
    },

    # ══════════════════════════════════════════════════════
    # SECTION 7 — ADDITIONAL CAREER & PLACEMENT ENTRIES
    # ══════════════════════════════════════════════════════

    {
        "id": "career-core-engineering",
        "category": "career",
        "title": "Career paths for core engineering backgrounds (non-data)",
        "text": (
            "Students from core engineering backgrounds (Mechanical, Automobile, Aerospace, "
            "Civil, Electrical, Chemical, Robotics) have strong options beyond data science. "
            "Core engineering roles: Design/CAD-CAE Engineer, Manufacturing/Production Engineer, "
            "Automotive/EV Engineer, Aerospace Engineer, Robotics Engineer, "
            "Automation/Control Engineer, Embedded Systems Engineer, Power/Electrical Engineer, "
            "Civil/Structural Engineer, Process/Chemical Engineer, Quality/R&D Engineer. "
            "For those wanting to add AI/data skills to a core path: "
            "Predictive maintenance (ME/EE), autonomous vehicles (Auto/EE), "
            "simulation-driven ML (Aerospace), edge AI (ECE/Robotics), "
            "bioinformatics (Biotech), process optimization (Chemical/Industrial). "
            "Our PGPDS and AI Engineering programs complement core engineering for hybrid roles. "
            "Recommended path: deepen core skills first, add Python and domain-specific ML as "
            "a second layer to stand out in niche roles."
        ),
    },
    {
        "id": "career-cybersecurity-path",
        "category": "career",
        "title": "Career path in cybersecurity — how to get started",
        "text": (
            "Cybersecurity is a high-demand, high-growth field. Entry paths: "
            "1. Security Analyst: monitor SIEM, respond to alerts, write incident reports. "
            "2. Network Security Engineer: configure firewalls, VPNs, IDS/IPS. "
            "3. Penetration Tester / Ethical Hacker: find vulnerabilities before attackers do. "
            "4. Cloud Security Engineer: secure AWS/Azure/GCP infrastructure and identities. "
            "5. AI Security / ML SecOps: secure LLM deployments, detect adversarial attacks. "
            "Key certifications to target: CompTIA Security+, CEH, OSCP, AWS Security Specialty. "
            "Core skills: networking (TCP/IP, OSI model), Linux, Python scripting, SIEM tools "
            "(Splunk, ELK), OWASP Top 10, incident response, cloud security basics. "
            "Our Cybersecurity Fundamentals program provides the CompTIA Security+-aligned "
            "foundation. Combine with real-world CTF practice (HackTheBox, TryHackMe). "
            "Starting salary range in India: ₹4–8 LPA for entry level; "
            "₹12–25 LPA for experienced with OSCP/cloud certifications."
        ),
    },
    {
        "id": "placement-outcome-data",
        "category": "placement",
        "title": "Placement outcomes — roles, salary bands, and top hiring companies",
        "text": (
            "PGPDS graduates are placed as: Data Analyst, Junior Data Scientist, "
            "ML Engineer, BI Analyst, Business Analyst, and Data Engineer. "
            "AI Engineering Track graduates are placed as: AI Engineer, LLM Engineer, "
            "MLOps Engineer, AI Product Analyst. "
            "Cybersecurity graduates: Security Analyst, SOC Analyst, Network Security Admin. "
            "Business Analytics: Business Analyst, BI Developer, Analytics Consultant. "
            "Salary bands (India, 2024–25): "
            "Fresher Data Analyst ₹3.5–6 LPA; Junior Data Scientist ₹5–9 LPA; "
            "ML/AI Engineer ₹6–12 LPA (fresher), ₹12–22 LPA (1–3 yrs experience); "
            "Cybersecurity Analyst ₹4–8 LPA; Business Analyst ₹4–7 LPA. "
            "Top hiring partners include analytics consulting firms, e-commerce companies, "
            "fintech startups, IT services majors, and BFSI organizations across Bengaluru, "
            "Hyderabad, Mumbai, Pune, and Kolkata. "
            "Placement rate: 80%+ of eligible, active students placed within 3 months of completion."
        ),
    },
]

