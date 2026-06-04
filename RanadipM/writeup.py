WRITEUP_MD = r"""
## AI & Cybersecurity Integrated Assignment — Design Document

A secure, Generative-AI student-support platform for a mid-sized training organization.
This running app *is* the implementation of the design below.

---

### Part 1 — AI Solution Design

**System overview.** A Retrieval-Augmented, multi-agent assistant. A central
**Supervisor agent** routes each query to a specialised sub-agent
(Course/FAQ, Troubleshooting, Placement, Career). Generative AI writes the
natural-language answers; agentic workflows handle multi-step tasks. All answers
are grounded in the organization's knowledge base via **RAG**, so the model does
not invent course or placement facts.

**Where Generative AI is used**
- Natural-language answers for course, troubleshooting and placement queries.
- Personalized career guidance synthesizing the student profile with role context.
- Summarization, rewriting, and query-intent understanding.

**Where agentic workflows are used**
- Supervisor routing to the right specialised agent.
- Tool-using sub-agents (placement → jobs DB, career → profile, troubleshoot → ticketing).
- Multi-step career planning: gather profile → retrieve → reason about gaps → produce a plan.
- A RAG retrieval loop before every generation to reduce hallucination.

**Data flow.** ingress (auth, rate-limit, input guardrails) → routing → RAG retrieval
→ generation → output guardrail (redaction) → persistence (encrypted app DB + audit log).
Sensitive PII never enters the prompt unless essential and is masked in logs.

---

### Part 2 — Cybersecurity & Network Design

**A. Network architecture.** Three-tier segmentation. Public users reach only a
load balancer/WAF in a DMZ. The app/API tier sits in a private subnet. The database
sits in an isolated subnet with **no internet route**. Firewalls enforce traffic only
in the allowed direction between adjacent tiers.

| Zone | Subnet | Internet reachable? |
|---|---|---|
| DMZ / Public | 192.168.10.0/24 | Inbound 443 only |
| App / API | 192.168.20.0/24 | No direct inbound |
| Database | 192.168.30.0/24 | No internet route |
| Management | 192.168.40.0/24 | VPN only |

**B. Secure communication.** TLS 1.2+/1.3 for all external traffic; WAF terminates
TLS with auto-renewed certs and HSTS. Internal service calls use mTLS / signed
short-lived tokens; secrets live in a vault. A user connection: TLS handshake →
encrypted channel + login token → each request authenticated at the gateway over
TLS → DB queried over an encrypted internal link.

**C. Access control.** Least-privilege **RBAC** enforced server-side on every request;
MFA for Admin/Staff; session timeouts and lockouts. Firewalls default-deny:
Internet→DMZ only 443; DMZ→App only the app port; App→DB only the DB port from the
app subnet; management via VPN only. Data encrypted at rest (AES-256, passwords
hashed with bcrypt/Argon2) and in transit; keys rotated via KMS.

**D. Risks & mitigations**
- **DDoS / API overload** → WAF, rate limits & quotas, autoscaling with cost ceilings, CDN.
- **Unauthorized access** → least-privilege RBAC, MFA, short-lived tokens, segmentation.
- **Data leakage** → PII masking in logs, output redaction, encryption, field-filtering.
- **Phishing / credential theft** → MFA, awareness training, anomaly detection, re-auth.
- **Prompt injection (AI-specific)** → input guardrails, instruction/content separation, scoped tools.

**E. Monitoring.** Track auth events, API usage, data access, AI/guardrail events, and
infra/firewall logs. Centralize into a **SIEM** with thresholds and anomaly detection;
alert on failed-login spikes, abnormal API volume, new geographies, mass exports.

---

### Part 3 — Critical Thinking

**1. Incorrect career advice — detect & fix.** Detect via user feedback, scheduled
evaluation against a golden Q&A set, guardrail/hallucination flags, and staff
spot-checks. Fix by reproducing failures, improving the RAG knowledge base, tightening
prompts/guardrails or rolling back, then re-testing on the eval set and adding the cases
to a regression suite.

**2. Leaked API key.** *Immediate:* revoke/rotate the key, invalidate derived sessions,
inspect logs for misuse and spend, block suspicious sources, notify stakeholders.
*Long-term:* secrets manager, short-lived auto-rotated keys, least-privilege scoping,
CI secret-scanning, spend/rate alerts, and a root-cause review.

**3. Preventing student-data exposure.** Data minimization (only needed data reaches the
model, PII masked), access control so an agent retrieves only entitled records, output
guardrails that redact PII, encryption at rest and in transit, log masking, prompt-injection
defenses, and periodic privacy reviews / red-teaming.

---

*This app demonstrates the input guardrail, RBAC, RAG grounding, agent routing,
output redaction, and audit logging described above — live, in the other tabs.*
"""
