"""
Screen Registry (V2 Preparation)
---------------------------------
Metadata-driven screen generation.

Future capabilities:
- Screen UI JSX generation
- Navigation type (stack, tab, drawer)
- Required dependencies
- Route parameters
- Component inference

Current: Basic metadata for future AI code generation
"""

from typing import Dict, List, Optional


# --------------------------------------------------
# Screen metadata definitions
# --------------------------------------------------

SCREEN_REGISTRY: List[Dict] = [
    {
        "id": "Home",
        "label": "Home Screen",
        "description": "Main landing screen",
        "navigation_type": "stack",
        "requires_auth": False,
        "dependencies": [],
        "route_params": [],
        "suggested_components": ["FlatList", "TouchableOpacity", "Image"],
        "ai_generation_prompt": "Create a modern home screen with a welcome message and navigation buttons",
    },
    {
        "id": "Login",
        "label": "Login Screen",
        "description": "User authentication login",
        "navigation_type": "stack",
        "requires_auth": False,
        "dependencies": ["react-hook-form", "yup"],
        "route_params": [],
        "suggested_components": ["TextInput", "AppButton", "KeyboardAvoidingView"],
        "ai_generation_prompt": "Create a login form with email/password fields, validation, and submit button",
    },
    {
        "id": "Signup",
        "label": "Signup Screen",
        "description": "User registration",
        "navigation_type": "stack",
        "requires_auth": False,
        "dependencies": ["react-hook-form", "yup"],
        "route_params": [],
        "suggested_components": ["TextInput", "AppButton", "KeyboardAvoidingView"],
        "ai_generation_prompt": "Create a signup form with name, email, password fields and validation",
    },
    {
        "id": "Profile",
        "label": "Profile Screen",
        "description": "User profile and settings",
        "navigation_type": "stack",
        "requires_auth": True,
        "dependencies": ["@react-native-async-storage/async-storage"],
        "route_params": [],
        "suggested_components": ["Image", "Text", "AppButton", "ScrollView"],
        "ai_generation_prompt": "Create a user profile screen with avatar, user info, and edit/logout buttons",
    },
    {
        "id": "Settings",
        "label": "Settings Screen",
        "description": "App settings and preferences",
        "navigation_type": "stack",
        "requires_auth": True,
        "dependencies": [],
        "route_params": [],
        "suggested_components": ["Switch", "Text", "ScrollView"],
        "ai_generation_prompt": "Create a settings screen with toggles for notifications, theme, language",
    },
    {
        "id": "Notifications",
        "label": "Notifications Screen",
        "description": "Push notifications list",
        "navigation_type": "stack",
        "requires_auth": True,
        "dependencies": [],
        "route_params": [],
        "suggested_components": ["FlatList", "TouchableOpacity", "Badge"],
        "ai_generation_prompt": "Create a notifications list with timestamp, message, and read/unread status",
    },
    {
        "id": "Chat",
        "label": "Chat Screen",
        "description": "Messaging interface",
        "navigation_type": "stack",
        "requires_auth": True,
        "dependencies": [],
        "route_params": ["chatId", "recipientName"],
        "suggested_components": ["FlatList", "TextInput", "KeyboardAvoidingView"],
        "ai_generation_prompt": "Create a chat interface with message bubbles, input field, and send button",
    },
    {
        "id": "Subscription",
        "label": "Subscription Screen",
        "description": "In-app purchases and subscriptions",
        "navigation_type": "stack",
        "requires_auth": True,
        "dependencies": [],
        "route_params": [],
        "suggested_components": ["ScrollView", "AppButton", "Text"],
        "ai_generation_prompt": "Create a subscription screen with pricing tiers, features list, and purchase buttons",
    },
    {
        "id": "Onboarding",
        "label": "Onboarding Screen",
        "description": "First-time user onboarding",
        "navigation_type": "stack",
        "requires_auth": False,
        "dependencies": [],
        "route_params": [],
        "suggested_components": ["ScrollView", "Image", "AppButton"],
        "ai_generation_prompt": "Create an onboarding carousel with app features, images, and get started button",
    },
]


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def get_screen_metadata(screen_id: str) -> Optional[Dict]:
    """
    Get metadata for a screen by ID.
    
    Args:
        screen_id: Screen identifier
    
    Returns:
        Screen metadata dict or None if not found
    """
    for screen in SCREEN_REGISTRY:
        if screen["id"] == screen_id:
            return screen
    return None


def get_all_screens() -> List[Dict]:
    """Get all screen metadata."""
    return SCREEN_REGISTRY


def get_screens_requiring_auth() -> List[str]:
    """Get list of screen IDs that require authentication."""
    return [s["id"] for s in SCREEN_REGISTRY if s["requires_auth"]]


def get_screen_dependencies(screen_ids: List[str]) -> List[str]:
    """
    Aggregate dependencies from multiple screens.
    
    Args:
        screen_ids: List of screen IDs
    
    Returns:
        Unique list of dependencies
    """
    deps = set()
    
    for screen_id in screen_ids:
        metadata = get_screen_metadata(screen_id)
        if metadata:
            deps.update(metadata["dependencies"])
    
    return sorted(deps)


def get_screen_navigation_types(screen_ids: List[str]) -> Dict[str, List[str]]:
    """
    Group screens by navigation type.
    
    Args:
        screen_ids: List of screen IDs
    
    Returns:
        Dict mapping navigation type to screen IDs
    """
    nav_types: Dict[str, List[str]] = {}
    
    for screen_id in screen_ids:
        metadata = get_screen_metadata(screen_id)
        if metadata:
            nav_type = metadata["navigation_type"]
            if nav_type not in nav_types:
                nav_types[nav_type] = []
            nav_types[nav_type].append(screen_id)
    
    return nav_types


# --------------------------------------------------
# V2: AI code generation (future)
# --------------------------------------------------

def generate_screen_code_ai(screen_id: str, provider: str = "gemini") -> str:
    """
    FUTURE: Generate screen JSX code using AI.
    
    Args:
        screen_id: Screen identifier
        provider: LLM provider to use
    
    Returns:
        Generated JSX code
    """
    # V2 implementation will use:
    # - Screen metadata
    # - AI generation prompt
    # - Suggested components
    # - Project theme/style
    
    raise NotImplementedError("AI code generation coming in V2")


def generate_redux_slice_ai(screen_id: str) -> str:
    """
    FUTURE: Generate Redux slice for screen using AI.
    
    Args:
        screen_id: Screen identifier
    
    Returns:
        Generated Redux slice code
    """
    raise NotImplementedError("AI Redux generation coming in V2")
