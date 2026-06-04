"""
Guardrails — demonstrates the security controls from Part 2 of the design.

- Input guardrail: blocks obvious prompt-injection attempts and flags PII.
- Output guardrail: redacts emails / phone numbers / long digit sequences
  (e.g. IDs) before a response leaves the system.

These are intentionally simple and transparent for the demo; production would
use a dedicated DLP / safety service.
"""

import re

# Patterns that look like prompt-injection / jailbreak attempts.
_INJECTION_PATTERNS = [
    r"ignore (all |the |your )?(previous|prior|above) (instructions|prompt)",
    r"disregard (your |the )?(system|previous) (prompt|instructions)",
    r"reveal (your |the )?(system )?prompt",
    r"you are now",
    r"developer mode",
    r"print (your |the )?(api )?key",
]

_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_PHONE = re.compile(r"\b(?:\+?\d{1,3}[\s-]?)?\d{10}\b")
_LONGNUM = re.compile(r"\b\d{12,}\b")  # e.g. Aadhaar-like / long IDs


def check_input(text: str) -> dict:
    """Return {'allowed': bool, 'reason': str, 'pii_flag': bool}."""
    lowered = text.lower()
    for pat in _INJECTION_PATTERNS:
        if re.search(pat, lowered):
            return {
                "allowed": False,
                "reason": "Possible prompt-injection attempt blocked by input guardrail.",
                "pii_flag": False,
            }
    pii = bool(_EMAIL.search(text) or _LONGNUM.search(text))
    return {"allowed": True, "reason": "", "pii_flag": pii}


def redact_output(text: str) -> tuple[str, int]:
    """Redact PII from model output. Returns (clean_text, num_redactions)."""
    count = 0

    def _sub(pattern, label, s):
        nonlocal count
        new, n = pattern.subn(f"[{label} REDACTED]", s)
        count += n
        return new

    text = _sub(_EMAIL, "EMAIL", text)
    text = _sub(_LONGNUM, "ID", text)
    text = _sub(_PHONE, "PHONE", text)
    return text, count
