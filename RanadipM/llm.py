"""
LLM client: Groq (primary) -> Gemini (fallback) -> deterministic mock.

Keys are read from environment variables / Streamlit secrets only.
Never hardcode keys. If no key is present, the app runs in MOCK mode,
which composes an answer from retrieved context so the demo still works.
"""

import os


def _get_key(name: str) -> str | None:
    val = os.environ.get(name)
    if val:
        return val
    # Streamlit secrets (optional)
    try:
        import streamlit as st

        return st.secrets.get(name)  # type: ignore
    except Exception:
        return None


def active_backend() -> str:
    if _get_key("GROQ_API_KEY"):
        return "Groq (llama-3.3-70b)"
    if _get_key("GEMINI_API_KEY"):
        return "Gemini (gemini-1.5-flash)"
    return "Mock (no key — retrieval-grounded template)"


def _call_groq(system: str, prompt: str) -> str:
    from groq import Groq

    client = Groq(api_key=_get_key("GROQ_API_KEY"))
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=700,
    )
    return resp.choices[0].message.content.strip()


def _call_gemini(system: str, prompt: str) -> str:
    import google.generativeai as genai

    genai.configure(api_key=_get_key("GEMINI_API_KEY"))
    model = genai.GenerativeModel(
        "gemini-1.5-flash", system_instruction=system
    )
    resp = model.generate_content(prompt)
    return resp.text.strip()


def _mock(system: str, prompt: str, context: str) -> str:
    if not context.strip():
        return (
            "I don't have information on that in the knowledge base yet. "
            "Please ask about courses, troubleshooting, placements, or career guidance, "
            "or contact staff for help."
        )
    return (
        "Based on our knowledge base:\n\n"
        + context
        + "\n\n*(Running in mock mode — add a GROQ_API_KEY or GEMINI_API_KEY "
        "to enable live generation.)*"
    )


def generate(system: str, prompt: str, context: str = "") -> tuple[str, str]:
    """
    Returns (answer, backend_used). Tries Groq, then Gemini, then mock.
    """
    if _get_key("GROQ_API_KEY"):
        try:
            return _call_groq(system, prompt), "Groq"
        except Exception as e:
            print("Groq failed, falling back:", e)
    if _get_key("GEMINI_API_KEY"):
        try:
            return _call_gemini(system, prompt), "Gemini"
        except Exception as e:
            print("Gemini failed, falling back:", e)
    return _mock(system, prompt, context), "Mock"
