"""
iOS Firebase Patches
-------------------
Native patches for Firebase setup on iOS.
"""

from typing import Dict


def setup_firebase() -> Dict:
    """Setup Firebase for iOS"""
    
    return {
        "type": "command",
        "description": "Setup Firebase for iOS",
        "bash_command": """
# Firebase setup instructions
echo "  📝 Manual step required: Add GoogleService-Info.plist to ios/ folder"
echo "  📝 Add Firebase pods to ios/Podfile"
echo "  📝 Run 'cd ios && pod install'"
""",
    }
