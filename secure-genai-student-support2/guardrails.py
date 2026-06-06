"""
Guardrails — demonstrates the security controls from Part 2 of the design.

- Input guardrail: blocks obvious prompt-injection attempts and flags PII.
- Output guardrail: redacts emails / phone numbers / long digit sequences
  (e.g. IDs) before a response leaves the system.

These are intentionally simple and transparent for the demo; production would
use a dedicated DLP / safety service. Regexes use bounded quantifiers to avoid
catastrophic backtracking (ReDoS) on adversarial input.
"""

import re
from typing import Tuple

# Patterns that look like prompt-injection / jailbreak attempts.
# NOTE: this is a transparent, demo-grade keyword/structure filter. It raises
# the bar against casual injection but is NOT a complete defense — a determined
# attacker can paraphrase or obfuscate around it. Production would pair this
# with an LLM-based / semantic guardrail and strict output validation.
_INJECTION_PATTERNS = [
    r"ignore (all |the |your )?(previous|prior|above) (instructions|prompt)",
    r"disregard (your |the )?(system|previous) (prompt|instructions)",
    r"reveal (your |the )?(system )?prompt",
    r"you are now",
    r"developer mode",
    r"print (your |the )?(api )?key",
    r"show (me )?(your |the )?(system )?(prompt|instructions)",
    r"bypass (your |the )?(rules|guardrails|filters)",
    # Additional jailbreak patterns
    r"act as (a |an )?(different|new|uncensored|unrestricted|evil|jailbroken)",
    r"pretend (you are|to be) (a |an )?(different|new|uncensored|unrestricted)",
    r"(forget|override) (your |all )?(previous |prior )?(rules|guidelines|training|instructions)",
    r"do anything now",
    r"dan mode",
    r"jailbreak",
    r"(output|print|repeat|echo) (your |the )?(system |original )?(prompt|instruction)",
    r"(respond|reply) (only |purely )?in (base64|hex|rot13)",
    r"translate (your |all )?(instructions|prompt) (to|into)",
]

# ReDoS-safe: bounded character-class lengths prevent catastrophic backtracking
# on crafted repetitive input. Email local/domain/TLD parts are length-capped.
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]{1,64}@[A-Za-z0-9-]{1,63}(?:\.[A-Za-z0-9-]{1,63}){0,4}\.[A-Za-z]{2,24}")
_PHONE = re.compile(r"\b(?:\+?91[\s\-]?)?[6-9]\d{9}\b")   # Indian mobile numbers
_PHONE_GENERIC = re.compile(r"\b(?:\+?\d{1,3}[\s-]?)?\d{10}\b")
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
    pii = bool(
        _EMAIL.search(text)
        or _LONGNUM.search(text)
        or _PHONE.search(text)
        or _PHONE_GENERIC.search(text)
    )
    return {"allowed": True, "reason": "", "pii_flag": pii}


def redact_output(text) -> Tuple[str, int]:
    """Redact PII from model output. Returns (clean_text, num_redactions).

    Defensive: tolerates non-string input (None, or a truncated/failed LLM
    response) by coercing to a string rather than crashing at runtime.
    """
    if text is None:
        return "", 0
    if not isinstance(text, str):
        text = str(text)
    count = 0

    def _sub(pattern, label, s):
        nonlocal count
        new, n = pattern.subn(f"[{label} REDACTED]", s)
        count += n
        return new

    text = _sub(_EMAIL, "EMAIL", text)
    text = _sub(_LONGNUM, "ID", text)
    text = _sub(_PHONE, "PHONE", text)
    text = _sub(_PHONE_GENERIC, "PHONE", text)
    return text, count
