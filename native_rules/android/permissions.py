"""
Android Permissions Patches
---------------------------
Native patches for AndroidManifest.xml permissions.
"""

from typing import Dict


def add_biometric_permission() -> Dict:
    """Add biometric authentication permission to AndroidManifest.xml"""
    
    return {
        "type": "file_edit",
        "description": "Add biometric permission",
        "file_path": "android/app/src/main/AndroidManifest.xml",
        "bash_command": """
# Add biometric permission if not exists
if ! grep -q "USE_BIOMETRIC" android/app/src/main/AndroidManifest.xml; then
  sed -i '' '/<manifest/a\\
    <uses-permission android:name="android.permission.USE_BIOMETRIC" />
' android/app/src/main/AndroidManifest.xml
fi
""",
    }


def add_notification_permission() -> Dict:
    """Add push notification permissions"""
    
    return {
        "type": "file_edit",
        "description": "Add notification permissions",
        "file_path": "android/app/src/main/AndroidManifest.xml",
        "bash_command": """
# Add notification permissions if not exists
if ! grep -q "POST_NOTIFICATIONS" android/app/src/main/AndroidManifest.xml; then
  sed -i '' '/<manifest/a\\
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />\\
    <uses-permission android:name="android.permission.VIBRATE" />
' android/app/src/main/AndroidManifest.xml
fi
""",
    }


def add_camera_permission() -> Dict:
    """Add camera permission"""
    
    return {
        "type": "file_edit",
        "description": "Add camera permission",
        "file_path": "android/app/src/main/AndroidManifest.xml",
        "bash_command": """
# Add camera permission if not exists
if ! grep -q "android.permission.CAMERA" android/app/src/main/AndroidManifest.xml; then
  sed -i '' '/<manifest/a\\
    <uses-permission android:name="android.permission.CAMERA" />
' android/app/src/main/AndroidManifest.xml
fi
""",
    }


def add_location_permission() -> Dict:
    """Add location permissions"""
    
    return {
        "type": "file_edit",
        "description": "Add location permissions",
        "file_path": "android/app/src/main/AndroidManifest.xml",
        "bash_command": """
# Add location permissions if not exists
if ! grep -q "ACCESS_FINE_LOCATION" android/app/src/main/AndroidManifest.xml; then
  sed -i '' '/<manifest/a\\
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />\\
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
' android/app/src/main/AndroidManifest.xml
fi
""",
    }
