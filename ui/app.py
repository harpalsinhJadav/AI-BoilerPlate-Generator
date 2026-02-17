import streamlit as st

from core.generator_engine import build_project_config
from output.bash_script_generator import generate_bash_script
from core.feature_registry import (
    get_all_features,
    collect_dependencies,
    collect_native_requirements,
)
from core.screen_registry import get_all_screens
from ai.feature_inference import infer_features
from ai.screen_inference import infer_screens
from ai.llm_provider import get_available_providers
from config.api_keys import validate_api_keys


# --------------------------------------------------
# Page config
# --------------------------------------------------

st.set_page_config(
    page_title="Mobile AI Boilerplate Generator",
    page_icon="📱",
    layout="wide",
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #61dafb;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4a90e2;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .user-added {
        background-color: #fff3cd;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
    .ai-selected {
        background-color: #d1ecf1;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #17a2b8;
    }
    </style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Session state initialization
# --------------------------------------------------

if "ai_detected" not in st.session_state:
    st.session_state.ai_detected = False

if "detected_features" not in st.session_state:
    st.session_state.detected_features = []

if "detected_screens" not in st.session_state:
    st.session_state.detected_screens = []

if "user_added_features" not in st.session_state:
    st.session_state.user_added_features = []

if "user_added_libraries" not in st.session_state:
    st.session_state.user_added_libraries = []

if "user_added_screens" not in st.session_state:
    st.session_state.user_added_screens = []

if "generated" not in st.session_state:
    st.session_state.generated = False


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown('<h1 class="main-header">📱 Mobile AI Boilerplate Generator</h1>', unsafe_allow_html=True)

st.markdown(
    """
    <div style='text-align: center; margin-bottom: 2rem;'>
    Generate <strong>production-ready React Native projects</strong> with 
    <strong>AI feature detection</strong> + <strong>native automation</strong> + <strong>runnable setup script</strong>
    </div>
    """,
    unsafe_allow_html=True
)

# API Key Status
providers = get_available_providers()

if providers:
    st.success(f"✅ AI Enabled: {', '.join(providers).upper()}")
else:
    st.warning("⚠️ AI Disabled: No API keys configured. Using keyword-based fallback.")
    with st.expander("ℹ️ How to enable AI"):
        st.markdown("""
        1. Copy `.env.template` to `.env`
        2. Add your API key:
           - **Gemini** (recommended): https://makersuite.google.com/app/apikey
           - **OpenAI**: https://platform.openai.com/api-keys
        3. Restart the application
        """)

st.divider()


# --------------------------------------------------
# Step 1: Project Configuration
# --------------------------------------------------

st.markdown('<h2 class="sub-header">📋 Step 1: Project Configuration</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    app_name = st.text_input(
        "App Name",
        value="MyAwesomeApp",
        help="No spaces. Used as project folder name (will be sanitized to PascalCase).",
    )

    stack = st.selectbox(
        "Tech Stack",
        options=["React Native CLI", "Expo"],
        index=0,
        help="Choose your React Native framework"
    )

with col2:
    automation_mode = st.selectbox(
        "Native Automation Mode",
        options=[
            "Safe automatic + fallback (recommended)",
            "Fully automatic",
        ],
        index=0,
        help="How to handle native Android/iOS configuration"
    )

description = st.text_area(
    "App Description",
    height=120,
    placeholder="E.g., Fitness tracking app with user authentication, workout logging, progress charts, push notifications, and social sharing features...",
    help="Describe your app's features. AI will detect required libraries and screens."
)

st.divider()


# --------------------------------------------------
# Step 2: AI Detection
# --------------------------------------------------

st.markdown('<h2 class="sub-header">🤖 Step 2: Run AI Detection</h2>', unsafe_allow_html=True)

st.markdown("Click below to let AI analyze your description and suggest features, libraries, and screens.")

detect_clicked = st.button(
    "🔍 Run AI Detection",
    type="primary",
    use_container_width=True,
    disabled=not description.strip()
)

if detect_clicked:
    with st.spinner("🧠 AI is analyzing your description..."):
        # Normalize stack
        stack_normalized = "rn_cli" if stack == "React Native CLI" else "expo"
        
        # Run AI detection
        st.session_state.detected_features = infer_features(description, stack_normalized)
        st.session_state.detected_screens = infer_screens(description)
        st.session_state.ai_detected = True
        
    st.success("✅ AI detection complete! Review and customize below.")
    st.rerun()

st.divider()


# --------------------------------------------------
# Step 3: Features & Libraries Selection
# --------------------------------------------------

if st.session_state.ai_detected:
    
    st.markdown('<h2 class="sub-header">🧩 Step 3: Select Features & Libraries</h2>', unsafe_allow_html=True)
    
    # Get all available features
    all_features = get_all_features()
    stack_normalized = "rn_cli" if stack == "React Native CLI" else "expo"
    
    # Filter features by stack
    available_features = [f for f in all_features if stack_normalized in f["stacks"]]
    
    # Features Section
    st.markdown("### 📦 Features")
    st.markdown("Select the features you want in your project. **Blue** = AI detected, **Yellow** = User added")
    
    # Create columns for better layout
    feat_cols = st.columns(3)
    
    selected_feature_ids = []
    
    for idx, feature in enumerate(available_features):
        col = feat_cols[idx % 3]
        
        with col:
            # Check if AI detected this feature
            is_ai_detected = feature["id"] in st.session_state.detected_features
            
            # Default checked if AI detected or if it's a default feature
            default_checked = is_ai_detected or feature["default"]
            
            # Add styling indicator
            if is_ai_detected:
                st.markdown(f'<div class="ai-selected">🤖 AI Detected</div>', unsafe_allow_html=True)
            
            checked = st.checkbox(
                feature["label"],
                value=default_checked,
                key=f"feature_{feature['id']}",
                help=f"{feature.get('description', 'No description available')}"
            )
            
            if checked:
                selected_feature_ids.append(feature["id"])
    
    # Add custom feature
    st.markdown("#### ➕ Add Custom Feature")
    
    col_input, col_button = st.columns([3, 1])
    
    with col_input:
        custom_feature = st.text_input(
            "Custom Feature ID",
            placeholder="e.g., custom_analytics",
            key="custom_feature_input",
            label_visibility="collapsed"
        )
    
    with col_button:
        if st.button("Add Feature", key="add_custom_feature"):
            if custom_feature and custom_feature not in st.session_state.user_added_features:
                st.session_state.user_added_features.append(custom_feature)
                st.rerun()
    
    # Display user-added features
    if st.session_state.user_added_features:
        st.markdown("**User-Added Features:**")
        for user_feat in st.session_state.user_added_features:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f'<div class="user-added">👤 {user_feat}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("❌", key=f"remove_feat_{user_feat}"):
                    st.session_state.user_added_features.remove(user_feat)
                    st.rerun()
            
            # Add to selected if checkbox is checked
            if st.checkbox(f"Include {user_feat}", value=True, key=f"include_feat_{user_feat}"):
                selected_feature_ids.append(user_feat)
    
    st.divider()
    
    # Libraries Section
    st.markdown("### 📚 Additional Libraries")
    st.markdown("Add extra npm packages not covered by features above")
    
    col_lib_input, col_lib_button = st.columns([3, 1])
    
    with col_lib_input:
        custom_library = st.text_input(
            "Library Name",
            placeholder="e.g., react-native-svg, lodash, dayjs",
            key="custom_library_input",
            label_visibility="collapsed"
        )
    
    with col_lib_button:
        if st.button("Add Library", key="add_custom_library"):
            if custom_library and custom_library not in st.session_state.user_added_libraries:
                st.session_state.user_added_libraries.append(custom_library)
                st.rerun()
    
    # Display user-added libraries
    selected_libraries = []
    if st.session_state.user_added_libraries:
        st.markdown("**Added Libraries:**")
        for lib in st.session_state.user_added_libraries:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f'<div class="user-added">📦 {lib}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("❌", key=f"remove_lib_{lib}"):
                    st.session_state.user_added_libraries.remove(lib)
                    st.rerun()
            
            if st.checkbox(f"Include {lib}", value=True, key=f"include_lib_{lib}"):
                selected_libraries.append(lib)
    
    st.divider()
    
    # Screens Section
    st.markdown("### 📱 Screens")
    st.markdown("Select screens to generate. **Blue** = AI detected, **Yellow** = User added")
    
    # Get all available screens
    all_screens_registry = get_all_screens()
    
    # Create columns for screens
    screen_cols = st.columns(3)
    
    selected_screen_ids = []
    
    for idx, screen in enumerate(all_screens_registry):
        col = screen_cols[idx % 3]
        
        with col:
            # Check if AI detected this screen
            is_ai_detected = screen["id"] in st.session_state.detected_screens
            
            # Default checked if AI detected
            default_checked = is_ai_detected
            
            # Add styling indicator
            if is_ai_detected:
                st.markdown(f'<div class="ai-selected">🤖 AI Detected</div>', unsafe_allow_html=True)
            
            checked = st.checkbox(
                screen["label"],
                value=default_checked,
                key=f"screen_{screen['id']}",
                help=f"{screen.get('description', 'No description available')}"
            )
            
            if checked:
                selected_screen_ids.append(screen["id"])
    
    # Add custom screen
    st.markdown("#### ➕ Add Custom Screen")
    
    col_screen_input, col_screen_button = st.columns([3, 1])
    
    with col_screen_input:
        custom_screen = st.text_input(
            "Custom Screen Name",
            placeholder="e.g., AnalyticsScreen, SettingsScreen",
            key="custom_screen_input",
            label_visibility="collapsed"
        )
    
    with col_screen_button:
        if st.button("Add Screen", key="add_custom_screen"):
            if custom_screen and custom_screen not in st.session_state.user_added_screens:
                st.session_state.user_added_screens.append(custom_screen)
                st.rerun()
    
    # Display user-added screens
    if st.session_state.user_added_screens:
        st.markdown("**User-Added Screens:**")
        for user_screen in st.session_state.user_added_screens:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f'<div class="user-added">👤 {user_screen}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("❌", key=f"remove_screen_{user_screen}"):
                    st.session_state.user_added_screens.remove(user_screen)
                    st.rerun()
            
            if st.checkbox(f"Include {user_screen}", value=True, key=f"include_screen_{user_screen}"):
                selected_screen_ids.append(user_screen)
    
    st.divider()
    
    # --------------------------------------------------
    # Step 4: Generate Project
    # --------------------------------------------------
    
    st.markdown('<h2 class="sub-header">🚀 Step 4: Generate Project Setup</h2>', unsafe_allow_html=True)
    
    # Summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Features Selected", len(selected_feature_ids))
    
    with col2:
        st.metric("Libraries Added", len(selected_libraries))
    
    with col3:
        st.metric("Screens Selected", len(selected_screen_ids))
    
    generate_clicked = st.button(
        "🎯 Generate Project Setup",
        type="primary",
        use_container_width=True,
    )
    
    # --------------------------------------------------
    # Generation logic
    # --------------------------------------------------
    
    if generate_clicked:
        try:
            with st.spinner("🔨 Generating your project setup..."):
                # Build base config
                final_config = build_project_config(
                    app_name=app_name,
                    stack_label=stack,
                    description=description,
                    automation_mode=automation_mode,
                )
                
                # Override with user selections
                final_config["features"] = selected_feature_ids
                final_config["screens"] = selected_screen_ids
                
                # Recalculate dependencies based on selected features
                deps_info = collect_dependencies(selected_feature_ids)
                native_info = collect_native_requirements(selected_feature_ids)
                
                final_config["dependencies"] = deps_info["dependencies"]
                final_config["dev_dependencies"] = deps_info["dev_dependencies"]
                final_config["native"] = native_info
                
                # Add user libraries
                if selected_libraries:
                    final_config["dependencies"].extend(selected_libraries)
                
                # Generate bash script
                script = generate_bash_script(final_config)
                
                st.session_state.generated = True
                st.session_state.config = final_config
                st.session_state.script = script
                
            st.success("✅ Project setup generated successfully!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Generation failed: {e}")
            import traceback
            st.code(traceback.format_exc())


# --------------------------------------------------
# Output section
# --------------------------------------------------

if st.session_state.generated:
    
    config = st.session_state.config
    script = st.session_state.script
    
    st.divider()
    st.markdown('<h2 class="sub-header">📋 Generated Configuration</h2>', unsafe_allow_html=True)
    
    # Summary tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📦 Features", "📚 Dependencies", "📱 Screens", "📜 Setup Script"])
    
    with tab1:
        st.markdown("### Selected Features")
        if config["features"]:
            for feat in config["features"]:
                st.markdown(f"- `{feat}`")
        else:
            st.info("No features selected")
    
    with tab2:
        st.markdown("### Production Dependencies")
        if config.get("dependencies"):
            st.code("\n".join(config["dependencies"]))
        else:
            st.info("No dependencies")
        
        st.markdown("### Dev Dependencies")
        if config.get("dev_dependencies"):
            st.code("\n".join(config["dev_dependencies"]))
        else:
            st.info("No dev dependencies")
    
    with tab3:
        st.markdown("### Generated Screens")
        if config["screens"]:
            for screen in config["screens"]:
                st.markdown(f"- `{screen}`")
        else:
            st.info("No screens selected")
    
    with tab4:
        st.markdown("### Complete Setup Script")
        st.code(script, language="bash")
        
        st.download_button(
            label="💾 Download setup.sh",
            data=script,
            file_name=f"{config['app_name']}_setup.sh",
            mime="text/x-sh",
            use_container_width=True,
        )
        
        st.info("""
        **Next Steps:**
        1. Download the script above
        2. Make it executable: `chmod +x setup.sh`
        3. Run it: `./setup.sh`
        4. Start developing!
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>📱 Mobile AI Boilerplate Generator v1.0 | Built with ❤️ using Streamlit & AI</p>
    <p>Generate production-ready React Native projects in seconds!</p>
</div>
""", unsafe_allow_html=True)
