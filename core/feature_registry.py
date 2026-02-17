"""
Feature Registry
----------------
Central source of truth for:

- Available features in React Native ecosystem
- Dependencies & dev dependencies
- Native Android/iOS patch requirements
- AI keyword matching
- Default selections

This file must remain PURE DATA + small helper functions.
No Streamlit / no generator logic here.
"""

from typing import Dict, List


# --------------------------------------------------
# Feature Definitions
# --------------------------------------------------

FEATURES: List[Dict] = [
    {
        "id": "navigation",
        "label": "React Navigation",
        "default": True,
        "stacks": ["rn_cli", "expo"],
        "dependencies": [
            "@react-navigation/native",
            "@react-navigation/stack",
            "@react-navigation/bottom-tabs",
            "react-native-screens",
            "react-native-safe-area-context",
        ],
        "dev_dependencies": [],
        "native": {"android": [], "ios": []},
        "screens": ["Home"],
        "description_keywords": ["navigation", "tabs", "routing"],
    },
    {
        "id": "redux",
        "label": "Redux Toolkit",
        "default": True,
        "stacks": ["rn_cli", "expo"],
        "dependencies": ["@reduxjs/toolkit", "react-redux"],
        "dev_dependencies": [],
        "native": {"android": [], "ios": []},
        "screens": [],
        "description_keywords": ["state", "redux", "store"],
    },
    {
        "id": "async_storage",
        "label": "AsyncStorage",
        "default": True,
        "stacks": ["rn_cli", "expo"],
        "dependencies": ["@react-native-async-storage/async-storage"],
        "dev_dependencies": [],
        "native": {"android": [], "ios": []},
        "screens": [],
        "description_keywords": ["storage", "cache", "persist"],
    },
    {
        "id": "auth",
        "label": "Authentication Flow",
        "default": True,
        "stacks": ["rn_cli", "expo"],
        "dependencies": [],
        "dev_dependencies": [],
        "native": {"android": [], "ios": []},
        "screens": ["Login", "Signup", "Profile"],
        "description_keywords": ["login", "signup", "auth", "user account"],
    },
    {
        "id": "axios",
        "label": "Axios API Client",
        "default": True,
        "stacks": ["rn_cli", "expo"],
        "dependencies": ["axios"],
        "dev_dependencies": [],
        "native": {"android": [], "ios": []},
        "screens": [],
        "description_keywords": ["api", "server", "backend", "http"],
    },
    {
        "id": "forms",
        "label": "React Hook Form + Yup",
        "default": True,
        "stacks": ["rn_cli", "expo"],
        "dependencies": ["react-hook-form", "yup"],
        "dev_dependencies": [],
        "native": {"android": [], "ios": []},
        "screens": ["Login", "Signup"],
        "description_keywords": ["form", "validation", "input"],
    },
    {
        "id": "theme",
        "label": "Dark / Light Theme",
        "default": True,
        "stacks": ["rn_cli", "expo"],
        "dependencies": [],
        "dev_dependencies": [],
        "native": {"android": [], "ios": []},
        "screens": [],
        "description_keywords": ["theme", "dark mode", "light mode"],
    },
    {
        "id": "i18n",
        "label": "Internationalization (i18next)",
        "default": False,
        "stacks": ["rn_cli", "expo"],
        "dependencies": ["i18next", "react-i18next"],
        "dev_dependencies": [],
        "native": {"android": [], "ios": []},
        "screens": [],
        "description_keywords": ["language", "translation", "multi language"],
    },
    {
        "id": "splash",
        "label": "Native Splash Screen",
        "default": True,
        "stacks": ["rn_cli"],
        "dependencies": ["react-native-splash-screen"],
        "dev_dependencies": [],
        "native": {
            "android": ["update_main_activity", "add_splash_theme"],
            "ios": ["update_app_delegate", "set_launch_screen"],
        },
        "screens": [],
        "description_keywords": ["splash", "launch screen"],
    },
    {
        "id": "biometric",
        "label": "Biometric Authentication",
        "default": False,
        "stacks": ["rn_cli", "expo"],
        "dependencies": ["react-native-biometrics"],
        "dev_dependencies": [],
        "native": {
            "android": ["add_biometric_permission"],
            "ios": ["add_faceid_permission"],
        },
        "screens": ["Login"],
        "description_keywords": ["biometric", "fingerprint", "face id"],
    },
    {
        "id": "notifications",
        "label": "Push Notifications",
        "default": False,
        "stacks": ["rn_cli", "expo"],
        "dependencies": [],
        "dev_dependencies": [],
        "native": {
            "android": ["add_notification_permission"],
            "ios": ["add_push_capability"],
        },
        "screens": [],
        "description_keywords": ["notification", "push"],
    },
]


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def get_all_features() -> List[Dict]:
    """Return full feature list."""
    return FEATURES


def get_default_features(stack: str) -> List[Dict]:
    """Return features enabled by default for a stack."""
    return [
        f for f in FEATURES
        if f["default"] and stack in f["stacks"]
    ]


def get_feature_by_id(feature_id: str) -> Dict:
    """Find a feature by its ID."""
    for f in FEATURES:
        if f["id"] == feature_id:
            return f
    raise ValueError(f"Feature not found: {feature_id}")


def collect_dependencies(feature_ids: List[str]) -> Dict[str, List[str]]:
    """
    Aggregate dependencies & dev dependencies
    from selected feature IDs.
    """
    deps = set()
    dev_deps = set()

    for fid in feature_ids:
        feature = get_feature_by_id(fid)
        deps.update(feature["dependencies"])
        dev_deps.update(feature["dev_dependencies"])

    return {
        "dependencies": sorted(deps),
        "dev_dependencies": sorted(dev_deps),
    }


def collect_native_requirements(feature_ids: List[str]) -> Dict:
    """Aggregate native patch requirements."""
    android = set()
    ios = set()

    for fid in feature_ids:
        feature = get_feature_by_id(fid)
        android.update(feature["native"]["android"])
        ios.update(feature["native"]["ios"])

    return {
        "android": sorted(android),
        "ios": sorted(ios),
    }
