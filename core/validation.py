"""
Input Validation Layer
----------------------
Sanitizes and validates user inputs before generation.

Prevents:
- Invalid app names
- Empty/malformed configurations
- Unsafe characters in bash scripts
"""

import re
from typing import Dict, List, Tuple


# --------------------------------------------------
# App name validation
# --------------------------------------------------

def sanitize_app_name(name: str) -> str:
    """
    Sanitize app name for safe use in:
    - File system paths
    - npm/npx commands
    - React Native project names
    
    Rules:
    - Remove spaces and special chars
    - Convert to PascalCase
    - Ensure starts with letter
    - Max 50 chars
    
    Returns:
        Sanitized app name
    
    Raises:
        ValueError: If name cannot be sanitized
    """
    
    if not name or not name.strip():
        raise ValueError("App name cannot be empty")
    
    # Remove all non-alphanumeric except spaces and underscores
    cleaned = re.sub(r'[^a-zA-Z0-9\s_]', '', name.strip())
    
    if not cleaned:
        raise ValueError("App name must contain at least one alphanumeric character")
    
    # Convert to PascalCase
    words = cleaned.replace('_', ' ').split()
    pascal_case = ''.join(word.capitalize() for word in words)
    
    # Ensure we have a valid name
    if not pascal_case:
        raise ValueError("App name must contain at least one alphanumeric character")
    
    # Ensure starts with letter
    if not pascal_case[0].isalpha():
        pascal_case = 'App' + pascal_case
    
    # Limit length
    if len(pascal_case) > 50:
        pascal_case = pascal_case[:50]
    
    return pascal_case


# --------------------------------------------------
# Description validation
# --------------------------------------------------

def sanitize_description(description: str) -> str:
    """
    Sanitize app description.
    
    - Trim whitespace
    - Remove potentially dangerous characters for bash
    - Limit length
    """
    
    if not description:
        return ""
    
    # Remove potentially dangerous bash characters
    cleaned = description.strip()
    
    # Remove backticks, dollar signs, and other bash special chars
    dangerous_chars = ['`', '$', '!', '|', '&', ';', '\n', '\r']
    for char in dangerous_chars:
        cleaned = cleaned.replace(char, ' ')
    
    # Collapse multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # Limit length
    max_length = 500
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    
    return cleaned


# --------------------------------------------------
# Feature validation
# --------------------------------------------------

def validate_features(
    feature_ids: List[str],
    valid_features: List[str],
) -> Tuple[List[str], List[str]]:
    """
    Validate feature IDs against registry.
    
    Args:
        feature_ids: User-selected feature IDs
        valid_features: Valid feature IDs from registry
    
    Returns:
        Tuple of (valid_ids, invalid_ids)
    """
    
    valid_set = set(valid_features)
    valid_ids = []
    invalid_ids = []
    
    for fid in feature_ids:
        if fid in valid_set:
            valid_ids.append(fid)
        else:
            invalid_ids.append(fid)
    
    return valid_ids, invalid_ids


# --------------------------------------------------
# Stack validation
# --------------------------------------------------

def validate_stack(stack_label: str) -> bool:
    """
    Validate stack selection.
    
    Returns:
        True if valid stack
    """
    valid_stacks = ["React Native CLI", "Expo"]
    return stack_label in valid_stacks


# --------------------------------------------------
# Full config validation
# --------------------------------------------------

def validate_project_config(config: Dict) -> Tuple[bool, List[str]]:
    """
    Validate complete project configuration.
    
    Args:
        config: Project configuration dict
    
    Returns:
        Tuple of (is_valid, error_messages)
    """
    
    errors = []
    
    # Check required fields
    required_fields = ["app_name", "stack", "features", "screens"]
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")
    
    # Validate app name
    if "app_name" in config:
        try:
            sanitize_app_name(config["app_name"])
        except ValueError as e:
            errors.append(f"Invalid app name: {e}")
    
    # Validate stack
    if "stack" in config:
        if config["stack"] not in ["rn_cli", "expo"]:
            errors.append(f"Invalid stack: {config['stack']}")
    
    # Validate features (at least one)
    if "features" in config:
        if not config["features"]:
            errors.append("At least one feature must be selected")
    
    # Validate screens (at least one)
    if "screens" in config:
        if not config["screens"]:
            errors.append("At least one screen must be generated")
    
    is_valid = len(errors) == 0
    
    return is_valid, errors


# --------------------------------------------------
# Bash safety
# --------------------------------------------------

def escape_bash_string(s: str) -> str:
    """
    Escape a string for safe use in bash scripts.
    
    Wraps in single quotes and escapes any single quotes inside.
    """
    # Replace single quotes with '\''
    escaped = s.replace("'", "'\\''")
    return f"'{escaped}'"


def validate_bash_command(command: str) -> bool:
    """
    Basic validation that a command doesn't contain obvious injection attempts.
    
    Returns:
        True if command appears safe
    """
    
    # Check for command chaining attempts
    dangerous_patterns = [
        r'&&',
        r'\|\|',
        r';',
        r'\$\(',
        r'`',
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, command):
            return False
    
    return True
