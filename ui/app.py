import streamlit as st

from core.generator_engine import build_project_config
from output.bash_script_generator import generate_bash_script


# --------------------------------------------------
# Page config
# --------------------------------------------------

st.set_page_config(
    page_title="Mobile AI Generator",
    page_icon="📱",
    layout="wide",
)


# --------------------------------------------------
# Session state
# --------------------------------------------------

if "generated" not in st.session_state:
    st.session_state.generated = False

if "script" not in st.session_state:
    st.session_state.script = ""


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📱 Mobile AI Boilerplate Generator")

st.markdown(
    """
Generate **production-ready React Native projects**  
using **AI feature detection + native automation + runnable setup script**.
"""
)

st.divider()


# --------------------------------------------------
# Project configuration
# --------------------------------------------------

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
        index=0,
    )

with col2:
    description = st.text_area(
        "App Description",
        height=140,
        placeholder="Fitness app with login, subscription, notifications...",
    )


# --------------------------------------------------
# Native automation mode
# --------------------------------------------------

st.subheader("🛠 Native Automation Mode")

automation_mode = st.radio(
    "Choose native automation behavior:",
    options=[
        "Safe automatic + fallback (recommended)",
        "Fully automatic",
    ],
    index=0,
)

st.divider()


# --------------------------------------------------
# Generate button
# --------------------------------------------------

generate_clicked = st.button(
    "🚀 Generate Project Setup",
    type="primary",
    use_container_width=True,
)


# --------------------------------------------------
# Generation logic
# --------------------------------------------------

if generate_clicked:
    try:
        config = build_project_config(
            app_name=app_name,
            stack_label=stack,
            description=description,
            automation_mode=automation_mode,
        )

        script = generate_bash_script(config)

        st.session_state.generated = True
        st.session_state.config = config
        st.session_state.script = script

    except Exception as e:
        st.error(f"Generation failed: {e}")


# --------------------------------------------------
# Output section
# --------------------------------------------------

if st.session_state.generated:

    config = st.session_state.config
    script = st.session_state.script

    st.divider()
    st.subheader("🧠 AI Detection Results")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Detected Features")
        st.code(", ".join(config["features"]))

    with col2:
        st.markdown("### Detected Screens")
        st.code(", ".join(config["screens"]))

    st.divider()
    st.subheader("📜 Generated setup.sh")

    st.code(script, language="bash")

    st.download_button(
        label="⬇️ Download setup.sh",
        data=script,
        file_name=f"{config['app_name']}_setup.sh",
        mime="text/x-sh",
        use_container_width=True,
    )

    st.success("V1 generator ready. Run the script in macOS/Linux terminal.")
