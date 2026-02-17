"""
AI Screen Inference
-------------------
Converts app description → required screen list.

Pipeline:

1. Try LLM semantic detection
2. If unavailable → deterministic keyword fallback
3. Always return a minimal runnable navigation set
"""

from typing import List, Set
import os

# Use centralized LLM provider
from ai.llm_provider import run_llm, is_llm_available


# --------------------------------------------------
# Core minimal screens (always needed)
# --------------------------------------------------

BASE_SCREENS = {"Home"}


# --------------------------------------------------
# Keyword → screen mapping (fallback engine)
# --------------------------------------------------

KEYWORD_SCREEN_MAP = {
    "login": {"Login"},
    "signup": {"Signup"},
    "auth": {"Login", "Signup"},
    "profile": {"Profile"},
    "settings": {"Settings"},
    "subscription": {"Subscription"},
    "payment": {"Subscription"},
    "chat": {"Chat"},
    "message": {"Chat"},
    "notification": {"Notifications"},
    "onboarding": {"Onboarding"},
    "intro": {"Onboarding"},
    "dashboard": {"Home"},
    "feed": {"Home"},
}


# --------------------------------------------------
# Deterministic fallback detection
# --------------------------------------------------

def keyword_screen_detection(description: str) -> List[str]:
    """
    Detect screens via simple keyword matching.
    Always ensures minimal runnable navigation.
    """
    description = description.lower()
    detected: Set[str] = set(BASE_SCREENS)

    for keyword, screens in KEYWORD_SCREEN_MAP.items():
        if keyword in description:
            detected.update(screens)

    # If auth implied but not explicit
    if any(k in description for k in ["user", "account", "login", "signup"]):
        detected.update({"Login", "Signup"})

    return sorted(detected)


# --------------------------------------------------
# LLM semantic detection
# --------------------------------------------------

def llm_screen_detection(description: str) -> List[str]:
    """
    Uses LLM (via centralized provider) to infer screens.
    Raises error if unavailable → caller handles fallback.
    """
    if not is_llm_available():
        raise RuntimeError("LLM not available")

    prompt = f"""You are a senior mobile UX architect.

From the app description below,
list the REQUIRED mobile app screens.

Rules:
- Return ONLY a comma-separated list of screen names.
- Use PascalCase (e.g., Login, UserProfile, Settings).
- Include Home screen for main apps.
- Include Login/Signup if authentication implied.
- Keep list minimal but complete.

App Description:
{description}

Answer:
"""

    result = run_llm(prompt, provider="gemini", temperature=0)

    raw = [s.strip() for s in result.split(",") if s.strip()]

    # Ensure base screen exists
    screens = set(raw) | BASE_SCREENS

    return sorted(screens)


# --------------------------------------------------
# Public API
# --------------------------------------------------

def infer_screens(description: str) -> List[str]:
    """
    Main entry point for generator engine.
    """

    if not description.strip():
        return sorted(BASE_SCREENS)

    try:
        return llm_screen_detection(description)
    except Exception:
        return keyword_screen_detection(description)
