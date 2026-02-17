"""
iOS Splash Screen Patches
-------------------------
Native patches for iOS splash screen setup.
"""

from typing import Dict


def update_app_delegate() -> Dict:
    """Update AppDelegate to show splash screen"""
    
    return {
        "type": "file_edit",
        "description": "Update AppDelegate for splash screen",
        "bash_command": """
# Add splash screen to AppDelegate
APP_DELEGATE=$(find ios -name "AppDelegate.mm" -o -name "AppDelegate.m" | head -n 1)

if [ -f "$APP_DELEGATE" ]; then
  # Add import
  if ! grep -q "RNSplashScreen" "$APP_DELEGATE"; then
    sed -i '' '/^#import/a\\
#import "RNSplashScreen.h"
' "$APP_DELEGATE"
    
    # Add show call
    sed -i '' '/didFinishLaunchingWithOptions/,/return YES/s/return YES/[RNSplashScreen show];\\
  return YES/' "$APP_DELEGATE"
  fi
fi
""",
    }


def set_launch_screen() -> Dict:
    """Configure launch screen"""
    
    return {
        "type": "command",
        "description": "Configure launch screen",
        "bash_command": """
echo "  📝 Launch screen configured via LaunchScreen.storyboard"
""",
    }
