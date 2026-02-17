"""
LLM Provider Layer
------------------
Centralized LLM interface to:

- Avoid duplicated provider imports
- Centralize API key management
- Enable multi-LLM future (Gemini, OpenAI, local)
- Provide consistent error handling

Public API:
    run_llm(prompt: str, provider: str = "gemini") -> str
"""

import os
from typing import Optional

# Optional LLM imports
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    
    GEMINI_AVAILABLE = True
except Exception:
    GEMINI_AVAILABLE = False

try:
    from langchain_openai import ChatOpenAI
    
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False


# --------------------------------------------------
# Provider implementations
# --------------------------------------------------

def _run_gemini(prompt: str, temperature: float = 0) -> str:
    """
    Run Gemini Pro via LangChain.
    Raises RuntimeError if unavailable.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY not found in environment")
    
    if not GEMINI_AVAILABLE:
        raise RuntimeError("langchain-google-genai not installed")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=temperature,
        google_api_key=api_key,
    )
    
    # Simple invoke for direct prompts
    result = llm.invoke(prompt)
    
    return result.content.strip()


def _run_openai(prompt: str, temperature: float = 0) -> str:
    """
    Run OpenAI GPT via LangChain.
    Raises RuntimeError if unavailable.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found in environment")
    
    if not OPENAI_AVAILABLE:
        raise RuntimeError("langchain-openai not installed")
    
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=temperature,
        api_key=api_key,
    )
    
    result = llm.invoke(prompt)
    
    return result.content.strip()


# --------------------------------------------------
# Public API
# --------------------------------------------------

def run_llm(
    prompt: str,
    provider: str = "gemini",
    temperature: float = 0,
) -> str:
    """
    Main entry point for all LLM calls.
    
    Args:
        prompt: The prompt to send to the LLM
        provider: "gemini" or "openai" (default: "gemini")
        temperature: LLM temperature (default: 0 for deterministic)
    
    Returns:
        LLM response as string
    
    Raises:
        RuntimeError: If provider unavailable or API key missing
        ValueError: If provider not supported
    """
    
    if provider == "gemini":
        return _run_gemini(prompt, temperature)
    elif provider == "openai":
        return _run_openai(prompt, temperature)
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def is_llm_available(provider: str = "gemini") -> bool:
    """
    Check if LLM provider is available.
    
    Args:
        provider: "gemini" or "openai"
    
    Returns:
        True if provider available and API key set
    """
    
    if provider == "gemini":
        return GEMINI_AVAILABLE and bool(os.getenv("GOOGLE_API_KEY"))
    elif provider == "openai":
        return OPENAI_AVAILABLE and bool(os.getenv("OPENAI_API_KEY"))
    else:
        return False


def get_available_providers() -> list[str]:
    """
    Get list of available LLM providers.
    
    Returns:
        List of provider names that are available
    """
    providers = []
    
    if is_llm_available("gemini"):
        providers.append("gemini")
    
    if is_llm_available("openai"):
        providers.append("openai")
    
    return providers
