import streamlit as st

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Mobile AI Generator",
    page_icon="📱",
    layout="wide",
)

# -------------------------------
# Session State Initialization
# -------------------------------
if "generated" not in st.session_state:
    st.session_state.generated = False

# -------------------------------
# Header
# -------------------------------
st.title("📱 Mobile AI Boilerplate Generator")
st.markdown(
    """
Generate **production-ready React Native projects** using  
AI-assisted feature detection, native automation, and runnable setup scripts.
"""
)

st.divider()

# -------------------------------
# Project Configuration Section
# -------------------------------
st.subheader("⚙️ Project Configuration")

col1, col2 = st.columns(2)

with col1:
    app_name = st.text_input(
        "App Name",
        value="MyAwesomeApp",
        help="No spaces. Used as project folder name.",
    )

    stack = st.selectbox(
        "Tech Stack",
        options=["React Native CLI", "Expo"],
        index=0,  # RN CLI default
        help="Choose your mobile framework.",
    )

with col2:
    description = st.text_area(
        "App Description",
        height=140,
        placeholder="Example: Fitness app with login, profile, subscription, push notifications...",
        help="AI will detect required features and screens from this.",
    )

# -------------------------------
# Native Automation Mode
# -------------------------------
st.subheader("🛠 Native Automation Mode")

automation_mode = st.radio(
    "Choose how native Android/iOS changes should be applied:",
    options=[
        "Safe automatic + fallback (recommended)",
        "Fully automatic",
    ],
    index=0,  # safe mode default
    help=(
        "Safe mode verifies file patches and shows manual steps if needed.\n"
        "Fully automatic applies changes without verification."
    ),
)

st.divider()

# -------------------------------
# Future AI Feature Preview (placeholder)
# -------------------------------
st.subheader("🤖 AI Feature Detection (Preview)")

st.info(
    "After generation, AI will:\n"
    "- Detect required **features** from description\n"
    "- Generate **screens, navigation, state, and API layer**\n"
    "- Prepare a **fully runnable project setup script**"
)

# -------------------------------
# Generate Button
# -------------------------------
generate_clicked = st.button(
    "🚀 Generate Project Setup",
    type="primary",
    use_container_width=True,
)

if generate_clicked:
    st.session_state.generated = True

    # Store minimal config in session
    st.session_state.config = {
        "app_name": app_name,
        "stack": stack,
        "description": description,
        "automation_mode": automation_mode,
    }

# -------------------------------
# Output Section (placeholder)
# -------------------------------
if st.session_state.generated:
    st.divider()
    st.subheader("📦 Generation Output")

    config = st.session_state.config

    st.success("Configuration captured successfully.")

    st.json(config)

    st.warning(
        "Next step: connect this UI to\n"
        "**AI inference → generator engine → native patch engine → bash script output**."
    )
