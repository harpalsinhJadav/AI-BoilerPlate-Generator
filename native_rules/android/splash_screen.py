"""
Android Splash Screen Patches
------------------------------
Native patches for splash screen setup.
"""

from typing import Dict


def update_main_activity() -> Dict:
    """Update MainActivity.kt to show splash screen"""
    
    return {
        "type": "file_edit",
        "description": "Update MainActivity for splash screen",
        "bash_command": """
# Add splash screen import and show call to MainActivity
if [ -f "android/app/src/main/java/com/*/MainActivity.kt" ]; then
  MAIN_ACTIVITY=$(find android/app/src/main/java -name "MainActivity.kt" | head -n 1)
  
  # Add import if not exists
  if ! grep -q "react-native-splash-screen" "$MAIN_ACTIVITY"; then
    sed -i '' '/^import/a\\
import org.devio.rn.splashscreen.SplashScreen
' "$MAIN_ACTIVITY"
    
    # Add show call in onCreate
    sed -i '' '/super.onCreate/a\\
    SplashScreen.show(this)
' "$MAIN_ACTIVITY"
  fi
fi
""",
    }


def add_splash_theme() -> Dict:
    """Add splash screen theme to styles.xml"""
    
    splash_theme = """
    <style name="SplashTheme" parent="Theme.AppCompat.Light.NoActionBar">
        <item name="android:windowBackground">@drawable/launch_screen</item>
    </style>
"""
    
    return {
        "type": "file_edit",
        "description": "Add splash theme to styles.xml",
        "bash_command": f"""
# Add splash theme to styles.xml
STYLES_FILE="android/app/src/main/res/values/styles.xml"

if [ -f "$STYLES_FILE" ]; then
  if ! grep -q "SplashTheme" "$STYLES_FILE"; then
    sed -i '' '/<\\/resources>/i\\
{splash_theme}
' "$STYLES_FILE"
  fi
fi
""",
    }
