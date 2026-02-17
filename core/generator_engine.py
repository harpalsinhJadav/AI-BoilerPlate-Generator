"""
Generator Engine
----------------
Central orchestrator that converts:

UI input → AI inference → registry aggregation → project_config

This module must stay:
- UI independent
- deterministic
- testable
"""

from typing import Dict, List

from ai.feature_inference import infer_features
from ai.screen_inference import infer_screens

from core.feature_registry import (
    collect_dependencies,
    collect_native_requirements,
    get_default_features,
)

from core.validation import (
    sanitize_app_name,
    sanitize_description,
    validate_project_config,
)


# --------------------------------------------------
# Stack normalization
# --------------------------------------------------

def normalize_stack(stack_label: str) -> str:
    """
    Convert UI label → internal stack key.
    """
    mapping = {
        "React Native CLI": "rn_cli",
        "Expo": "expo",
    }

    if stack_label not in mapping:
        raise ValueError(f"Unsupported stack: {stack_label}")

    return mapping[stack_label]


# --------------------------------------------------
# Feature resolution
# --------------------------------------------------

def resolve_features(description: str, stack: str) -> List[str]:
    """
    Determine final feature list using:
    - AI inference
    - defaults merge
    """
    inferred = set(infer_features(description, stack))
    defaults = {f["id"] for f in get_default_features(stack)}

    return sorted(inferred | defaults)


# --------------------------------------------------
# Screen resolution
# --------------------------------------------------

def resolve_screens(description: str) -> List[str]:
    """
    Determine required screens from description.
    """
    return infer_screens(description)


# --------------------------------------------------
# Build final project configuration
# --------------------------------------------------

def build_project_config(
    app_name: str,
    stack_label: str,
    description: str,
    automation_mode: str,
) -> Dict:
    """
    Main public function used by UI.

    Returns a normalized project configuration
    ready for script generation.
    """

    # --------------------------------------------------
    # Input validation & sanitization
    # --------------------------------------------------

    app_name = sanitize_app_name(app_name)
    description = sanitize_description(description)

    stack = normalize_stack(stack_label)

    # --------------------------------------------------
    # AI inference
    # --------------------------------------------------

    features = resolve_features(description, stack)
    screens = resolve_screens(description)

    # --------------------------------------------------
    # Dependency aggregation
    # --------------------------------------------------

    deps_info = collect_dependencies(features)
    native_info = collect_native_requirements(features)

    # --------------------------------------------------
    # Final normalized config
    # --------------------------------------------------

    project_config: Dict = {
        "app_name": app_name,
        "stack": stack,
        "description": description,
        "features": features,
        "screens": screens,
        "dependencies": deps_info["dependencies"],
        "dev_dependencies": deps_info["dev_dependencies"],
        "native": native_info,
        "automation_mode": automation_mode,
    }

    # --------------------------------------------------
    # Validate final config
    # --------------------------------------------------

    is_valid, errors = validate_project_config(project_config)

    if not is_valid:
        raise ValueError(f"Invalid project configuration: {', '.join(errors)}")

    return project_config
