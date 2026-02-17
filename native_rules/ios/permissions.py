"""
iOS Permissions Patches
-----------------------
Native patches for Info.plist permissions.
"""

from typing import Dict


def add_faceid_permission() -> Dict:
    """Add Face ID permission to Info.plist"""
    
    return {
        "type": "file_edit",
        "description": "Add Face ID permission",
        "bash_command": """
# Add Face ID permission to Info.plist
INFO_PLIST="ios/$(ls ios | grep '.xcodeproj' | sed 's/.xcodeproj//')/Info.plist"

if [ -f "$INFO_PLIST" ]; then
  /usr/libexec/PlistBuddy -c "Add :NSFaceIDUsageDescription string 'We use Face ID for secure authentication'" "$INFO_PLIST" 2>/dev/null || true
fi
""",
    }


def add_push_capability() -> Dict:
    """Add push notification capability"""
    
    return {
        "type": "command",
        "description": "Add push notification capability",
        "bash_command": """
echo "  📝 Manual step: Enable Push Notifications in Xcode capabilities"
""",
    }


def add_camera_permission() -> Dict:
    """Add camera permission to Info.plist"""
    
    return {
        "type": "file_edit",
        "description": "Add camera permission",
        "bash_command": """
# Add camera permission to Info.plist
INFO_PLIST="ios/$(ls ios | grep '.xcodeproj' | sed 's/.xcodeproj//')/Info.plist"

if [ -f "$INFO_PLIST" ]; then
  /usr/libexec/PlistBuddy -c "Add :NSCameraUsageDescription string 'We need camera access for photos'" "$INFO_PLIST" 2>/dev/null || true
fi
""",
    }


def add_location_permission() -> Dict:
    """Add location permissions to Info.plist"""
    
    return {
        "type": "file_edit",
        "description": "Add location permissions",
        "bash_command": """
# Add location permissions to Info.plist
INFO_PLIST="ios/$(ls ios | grep '.xcodeproj' | sed 's/.xcodeproj//')/Info.plist"

if [ -f "$INFO_PLIST" ]; then
  /usr/libexec/PlistBuddy -c "Add :NSLocationWhenInUseUsageDescription string 'We need your location'" "$INFO_PLIST" 2>/dev/null || true
  /usr/libexec/PlistBuddy -c "Add :NSLocationAlwaysUsageDescription string 'We need your location'" "$INFO_PLIST" 2>/dev/null || true
fi
""",
    }
