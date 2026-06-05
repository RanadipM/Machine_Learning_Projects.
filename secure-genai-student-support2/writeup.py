WRITEUP_MD = r"""
## AI & Cybersecurity Integrated Assignment — Design Document

**Applicant:** Ranadip | **Role:** AI & Cybersecurity SME | **Status:** Live deployed application

A secure, Generative-AI student-support platform for a mid-sized training organization.
This running app *is* the implementation of the design below — every section maps to a live feature.

---

### Part 1 — AI Solution Design

**System overview.** A Retrieval-Augmented, multi-agent assistant. A central
**Supervisor agent** routes each query to a specialised sub-agent
(Course/FAQ, Troubleshooting, Placement, Career, and System & Security). Generative AI writes the
natural-language answers; agentic workflows handle multi-step tasks. All answers
are grounded in the organization's verified knowledge base via **RAG**, so the model does
not invent course or placement facts.

**Where Generative AI is used**
- Natural-language answers for course, troubleshooting, and placement queries.
- Personalized career guidance synthesizing the student profile with role context.
- Summarization, rewriting, and query-intent understanding.
- Fallback graceful responses when the knowledge base has no matching entry.

**Where agentic workflows are used**
- Supervisor routing to the right specialised agent (5 specialists, keyword + context scoring).
- Tool-using sub-agents (placement → jobs DB, career → profile, troubleshoot → ticketing).
- Multi-step career planning: gather profile → retrieve → reason about gaps → produce a plan.
- A RAG retrieval loop before every generation to reduce hallucination.

**Data flow table**

| Stage | Component | What happens | Security control |
|---|---|---|---|
| 1. Ingress | WAF / Load Balancer | Rate-limit, TLS termination | HTTPS only, DDoS protection |
| 2. Auth | Auth Gateway | Token validation, MFA check | RBAC enforced server-side |
| 3. Input guardrail | `guardrails.check_input()` | Block injections, flag PII | Regex + pattern matching |
| 4. Route | Supervisor agent | Classify intent → assign specialist | Keyword scoring + tie-breakers |
| 5. Retrieve | TF-IDF RAG (demo) / ChromaDB (prod) | Top-k grounding passages | Scoped by category |
| 6. Generate | Groq (primary) → Gemini (fallback) | Answer from context only | Grounded prompt, temp=0.3 |
| 7. Output guardrail | `guardrails.redact_output()` | Strip emails, phones, IDs | PII redaction before display |
| 8. Persist | Encrypted app DB | Log audit event, store exchange | AES-256 at rest, TLS in transit |

Sensitive PII never enters the LLM prompt unless essential and is masked in logs.

---

### Part 2 — Cybersecurity & Network Design

**A. Network architecture.** Three-tier segmentation with a Management VLAN. Public users reach
only a load balancer/WAF in a DMZ. The app/API tier sits in a private subnet. The database sits
in an isolated subnet with **no internet route**. Firewalls enforce traffic only in the allowed
direction between adjacent tiers.

| Zone | Subnet | Internet reachable? | Hosts |
|---|---|---|---|
| DMZ / Public | 192.168.10.0/24 | Inbound port 443 only | Load balancer, WAF, CDN edge |
| App / API | 192.168.20.0/24 | No direct inbound | App server (192.168.20.10), API gateway |
| Database | 192.168.30.0/24 | No internet route | DB primary (192.168.30.10), replica (.11) |
| Management | 192.168.40.0/24 | VPN only (split-tunnel) | SIEM, jump host, admin workstations |

**B. Secure communication.** TLS 1.2+/1.3 for all external traffic; WAF terminates
TLS with auto-renewed Let's Encrypt certs and HSTS headers. Internal service calls use mTLS /
signed short-lived tokens; secrets live in a vault (HashiCorp Vault or AWS Secrets Manager).

Connection walkthrough (high-level):
1. Student browser initiates HTTPS — TLS 1.3 handshake with WAF, server cert verified.
2. Encrypted channel established; WAF inspects request (OWASP rules, rate limits).
3. WAF forwards to App server over an internal encrypted link (port 443, private subnet only).
4. App server validates JWT / session token, enforces RBAC role.
5. DB query issued over an encrypted connection (TLS, port 5432) within the DB subnet.
6. Response travels back through the same chain; output guardrail strips PII before delivery.

**C. Access control & security measures**

*User roles (RBAC):*
- **Student** — least privilege: own profile, courses, placements, and the AI assistant only.
- **Staff** — departmental: assigned student records, content management, placement data.
- **Admin** — elevated: system configuration, user management, full audit logs; all actions logged; MFA mandatory.

*Firewall rules (default-deny baseline):*

| From | To | Port | Action | Reason |
|---|---|---|---|---|
| Internet | DMZ WAF | 443 | ALLOW | Public HTTPS access |
| Internet | DMZ WAF | 80 | ALLOW → redirect | HTTP to HTTPS redirect only |
| Internet | Any other | * | DENY | No direct app/DB exposure |
| DMZ | App subnet | 443 | ALLOW | WAF → app server only |
| App subnet | DB subnet | 5432 | ALLOW | App → DB over private link |
| App subnet | Management | 514/syslog | ALLOW | Log shipping to SIEM |
| DB subnet | Internet | * | DENY | Database never calls outbound |
| Management | All | 22 (VPN) | ALLOW | SSH via VPN jump host only |
| Any → Any | * | * | DENY | Implicit default deny |

*Data protection:*
- At rest: AES-256 for the database; passwords hashed with bcrypt (cost factor ≥ 12) or Argon2id.
- In transit: TLS 1.2+/1.3 everywhere, including internal service calls.
- Key management: KMS with automatic rotation; keys scoped to least privilege.

**D. Risks & mitigations**

| Risk | What it is | Prevention |
|---|---|---|
| DDoS / API overload | Volumetric flood overwhelms the API, denying service | WAF + rate limits per key/IP; autoscaling with cost ceiling; CDN absorbs traffic |
| Unauthorized access | Attacker gains access to student or staff data | Least-privilege RBAC; MFA for Staff/Admin; short-lived tokens; brute-force lockout |
| Data leakage | PII or sensitive records exposed via AI output or logs | Output PII redaction; log masking; encryption at rest; field-level access control |
| Phishing / credential theft | Stolen credentials used to impersonate a user | MFA renders stolen passwords insufficient; anomaly detection; forced re-auth on suspicious logins |
| Prompt injection (AI-specific) | Attacker embeds instructions in input to hijack AI behaviour | Input guardrails (regex + pattern matching); instruction/content separation; scoped tool permissions; output validation |

**E. Monitoring**

Track: authentication events (login success/failure, MFA, lockouts), API usage (endpoint, caller,
status, latency, rate-limit hits), data-access events (who read/wrote which record), AI/agent
events (queries, retrieved sources, guardrail triggers, token usage), and infrastructure/firewall
events (denies, config changes, admin actions).

Centralize into a **SIEM** (e.g. ELK Stack or Splunk) with alerting thresholds:
- Failed login spike (> 5 failures / minute per IP) → alert + auto-block
- Abnormal API volume (> 3× baseline in a 10-min window) → alert + rate-cap
- Access from a new geography for a privileged account → alert + step-up auth
- Mass data-export pattern (> 100 records in one session) → alert + manual review

---

### Part 3 — Critical Thinking

**1. Incorrect career advice — detect & fix.**
Detect via: (a) in-app user feedback (thumbs-up/down, free-text report); (b) weekly automated
evaluation against a curated golden Q&A set with expected answers; (c) guardrail / hallucination
flags; (d) staff spot-checks of a random 5% of sessions. Fix by reproducing failing cases,
then addressing root cause — expand or correct the RAG knowledge base, tighten the agent prompt,
add validation rules, or roll back to a known-good prompt version. Re-test on the evaluation
set before redeploying; add the failure cases to a regression suite so the issue cannot silently recur.

**2. Leaked API key — immediate and long-term response.**
*Immediate:* revoke and rotate the key in the secrets manager within minutes; invalidate all
sessions derived from it; scan logs for unauthorized requests and unusual spend; block
suspicious source IPs; notify relevant stakeholders and document the incident timeline.
*Long-term:* enforce short-lived, auto-rotating keys via a vault; add CI/CD secret-scanning
(e.g. GitHub secret-scanner, truffleHog pre-commit hook); set real-time spend and rate alerts;
scope keys to the minimum required permissions; conduct a root-cause review to identify and
close the gap that caused the leak.

**3. Preventing student-data exposure from the AI.**
Data minimization ensures only the data needed for a specific answer reaches the model — the
prompt is constructed from retrieved knowledge-base excerpts, not raw student records. RBAC
ensures each agent retrieves only what the caller's role permits. Output guardrails strip emails,
phone numbers, and long ID strings before the response is shown. Logs mask PII fields at write
time. Encryption at rest and in transit protects stored data if a system is compromised.
Prompt-injection defenses prevent an attacker from crafting inputs that trick the model into
revealing data. Periodic privacy red-team exercises verify that no leakage path exists end-to-end.

---

*Every design decision above is implemented and demonstrable in this application's other tabs.*
"""
