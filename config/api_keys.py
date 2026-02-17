"""
API Key Configuration
---------------------
Centralized environment variable loading.

Loads from .env file if present, otherwise uses system environment.
"""

import os
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

def load_env_config():
    """
    Load environment variables from .env file if present.
    
    Searches for .env in:
    1. Current working directory
    2. Project root (parent of this file)
    """
    
    if not DOTENV_AVAILABLE:
        return
    
    # Try current directory first
    cwd_env = Path.cwd() / ".env"
    if cwd_env.exists():
        load_dotenv(cwd_env)
        return
    
    # Try project root
    project_root = Path(__file__).parent.parent
    root_env = project_root / ".env"
    if root_env.exists():
        load_dotenv(root_env)
        return


# Auto-load on import
load_env_config()


# --------------------------------------------------
# API key getters
# --------------------------------------------------

def get_google_api_key() -> Optional[str]:
    """Get Google API key from environment."""
    return os.getenv("GOOGLE_API_KEY")


def get_openai_api_key() -> Optional[str]:
    """Get OpenAI API key from environment."""
    return os.getenv("OPENAI_API_KEY")


def get_anthropic_api_key() -> Optional[str]:
    """Get Anthropic API key from environment (future)."""
    return os.getenv("ANTHROPIC_API_KEY")


# --------------------------------------------------
# Validation
# --------------------------------------------------

def validate_api_keys() -> dict[str, bool]:
    """
    Validate which API keys are configured.
    
    Returns:
        Dict mapping provider name to availability
    """
    return {
        "google": bool(get_google_api_key()),
        "openai": bool(get_openai_api_key()),
        "anthropic": bool(get_anthropic_api_key()),
    }


def get_configured_providers() -> list[str]:
    """
    Get list of providers with valid API keys.
    
    Returns:
        List of provider names
    """
    validation = validate_api_keys()
    return [name for name, valid in validation.items() if valid]
