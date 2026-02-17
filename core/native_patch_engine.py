"""
Native Patch Engine
-------------------
Zero manual Android/iOS setup.

Orchestrates native file patches based on feature requirements.

Flow:
1. Collect native requirements from features
2. Load appropriate patch rules
3. Generate patch instructions for bash script
4. Apply patches safely with fallback
"""

from typing import Dict, List
from native_rules.android import permissions as android_permissions
from native_rules.android import splash_screen as android_splash
from native_rules.android import firebase as android_firebase

from native_rules.ios import permissions as ios_permissions
from native_rules.ios import splash_screen as ios_splash
from native_rules.ios import firebase as ios_firebase


# --------------------------------------------------
# Patch rule registry
# --------------------------------------------------

ANDROID_PATCHES = {
    "add_biometric_permission": android_permissions.add_biometric_permission,
    "add_notification_permission": android_permissions.add_notification_permission,
    "add_camera_permission": android_permissions.add_camera_permission,
    "add_location_permission": android_permissions.add_location_permission,
    
    "update_main_activity": android_splash.update_main_activity,
    "add_splash_theme": android_splash.add_splash_theme,
    
    "setup_firebase": android_firebase.setup_firebase,
}

IOS_PATCHES = {
    "add_faceid_permission": ios_permissions.add_faceid_permission,
    "add_push_capability": ios_permissions.add_push_capability,
    "add_camera_permission": ios_permissions.add_camera_permission,
    "add_location_permission": ios_permissions.add_location_permission,
    
    "update_app_delegate": ios_splash.update_app_delegate,
    "set_launch_screen": ios_splash.set_launch_screen,
    
    "setup_firebase": ios_firebase.setup_firebase,
}


# --------------------------------------------------
# Patch generation
# --------------------------------------------------

def generate_android_patches(requirements: List[str]) -> List[Dict]:
    """
    Generate Android patch instructions.
    
    Args:
        requirements: List of Android patch IDs
    
    Returns:
        List of patch instruction dicts with:
        - type: "file_edit" | "file_create" | "command"
        - description: Human-readable description
        - instructions: Bash commands or file operations
    """
    
    patches = []
    
    for req in requirements:
        if req in ANDROID_PATCHES:
            patch_fn = ANDROID_PATCHES[req]
            patch = patch_fn()
            patches.append(patch)
    
    return patches


def generate_ios_patches(requirements: List[str]) -> List[Dict]:
    """
    Generate iOS patch instructions.
    
    Args:
        requirements: List of iOS patch IDs
    
    Returns:
        List of patch instruction dicts
    """
    
    patches = []
    
    for req in requirements:
        if req in IOS_PATCHES:
            patch_fn = IOS_PATCHES[req]
            patch = patch_fn()
            patches.append(patch)
    
    return patches


# --------------------------------------------------
# Bash script generation for patches
# --------------------------------------------------

def generate_patch_bash(patches: List[Dict], platform: str) -> str:
    """
    Convert patch instructions to bash script commands.
    
    Args:
        patches: List of patch dicts
        platform: "android" or "ios"
    
    Returns:
        Bash script string
    """
    
    if not patches:
        return ""
    
    script = f'\necho "🔧 Applying {platform.upper()} native patches..."\n'
    
    for patch in patches:
        patch_type = patch.get("type", "command")
        description = patch.get("description", "Applying patch")
        
        script += f'\necho "  - {description}"\n'
        
        if patch_type == "file_edit":
            # File edit using sed or similar
            script += patch.get("bash_command", "")
        
        elif patch_type == "file_create":
            # Create new file
            file_path = patch.get("file_path", "")
            content = patch.get("content", "")
            script += f'''
cat > "{file_path}" <<'EOF'
{content}
EOF
'''
        
        elif patch_type == "command":
            # Direct command
            script += patch.get("bash_command", "")
        
        script += "\n"
    
    return script


# --------------------------------------------------
# Public API
# --------------------------------------------------

def apply_native_patches(config: Dict) -> str:
    """
    Main entry point for native patch generation.
    
    Args:
        config: Project configuration with native requirements
    
    Returns:
        Bash script string with all native patches
    """
    
    native_reqs = config.get("native", {})
    android_reqs = native_reqs.get("android", [])
    ios_reqs = native_reqs.get("ios", [])
    
    # Generate patches
    android_patches = generate_android_patches(android_reqs)
    ios_patches = generate_ios_patches(ios_reqs)
    
    # Convert to bash
    android_bash = generate_patch_bash(android_patches, "android")
    ios_bash = generate_patch_bash(ios_patches, "ios")
    
    # Combine
    script = ""
    
    if android_bash:
        script += android_bash
    
    if ios_bash and config.get("stack") == "rn_cli":
        # iOS patches only for React Native CLI
        script += ios_bash
    
    return script
