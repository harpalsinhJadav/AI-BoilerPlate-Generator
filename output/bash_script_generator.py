"""
Bash Script Generator
---------------------
Converts project_config → runnable setup.sh script.
"""

from typing import Dict, List


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def _join(items: List[str]) -> str:
    """Join list safely for bash."""
    return " ".join(sorted(set(items))) if items else ""


# --------------------------------------------------
# Script sections
# --------------------------------------------------

def _script_header(app_name: str) -> str:
    return f"""#!/bin/bash
set -e

echo "🚀 Mobile AI Generator Setup"
echo "Project: {app_name}"
echo "-----------------------------------"
"""


def _project_init(config: Dict) -> str:
    app = config["app_name"]
    stack = config["stack"]

    if stack == "rn_cli":
        return f"""
echo "📱 Creating React Native CLI project..."
npx @react-native-community/cli@latest init {app}
cd {app}
"""
    elif stack == "expo":
        return f"""
echo "📱 Creating Expo project..."
npx create-expo-app@latest {app}
cd {app}
"""
    else:
        raise ValueError("Unsupported stack")


def _install_dependencies(config: Dict) -> str:
    deps = _join(config["dependencies"])
    dev_deps = _join(config["dev_dependencies"])

    script = "\necho \"📦 Installing dependencies...\"\n"

    if deps:
        script += f"npm install {deps}\n"

    if dev_deps:
        script += f"npm install -D {dev_deps}\n"

    return script


def _ios_pods(config: Dict) -> str:
    if config["stack"] != "rn_cli":
        return ""

    return """
echo "🍎 Installing iOS pods..."
cd ios
pod install
cd ..
"""


def _native_mode_notice(config: Dict) -> str:
    mode = config["automation_mode"]

    return f"""
echo "🛠 Native automation mode: {mode}"
echo "Native patch engine will be applied in next version."
"""


def _create_folders() -> str:
    return """
echo "📁 Creating source folders..."

mkdir -p src/screens
mkdir -p src/navigation
mkdir -p src/api
mkdir -p src/store
mkdir -p src/theme
"""


def _create_stub_files(config: Dict) -> str:
    screens = config["screens"]

    script = '\necho "🧩 Creating stub files..."\n'

    # Navigation stub
    script += """
cat > src/navigation/AppNavigator.js <<'EOF'
import React from 'react';
import { Text, View } from 'react-native';

export default function AppNavigator() {
  return (
    <View style={{flex:1,alignItems:'center',justifyContent:'center'}}>
      <Text>App Navigator Ready</Text>
    </View>
  );
}
EOF
"""

    # API client stub
    script += """
cat > src/api/client.js <<'EOF'
import axios from 'axios';

const api = axios.create({
  baseURL: "https://example.com/api",
});

export default api;
EOF
"""

    # Store stub
    script += """
cat > src/store/index.js <<'EOF'
export const store = {};
EOF
"""

    # Screen stubs
    for screen in screens:
        script += f"""
cat > src/screens/{screen}Screen.js <<'EOF'
import React from 'react';
import {{ View, Text }} from 'react-native';

export default function {screen}Screen() {{
  return (
    <View style={{flex:1,alignItems:'center',justifyContent:'center'}}>
      <Text>{screen} Screen</Text>
    </View>
  );
}}
EOF
"""

    return script


def _final_instructions(config: Dict) -> str:
    return f"""
echo "-----------------------------------"
echo "✅ Project setup complete!"
echo ""
echo "Next steps:"
echo "cd {config['app_name']}"
echo "npm start"
echo "npm run ios   # macOS only"
echo "npm run android"
"""


# --------------------------------------------------
# Public API
# --------------------------------------------------

def generate_bash_script(config: Dict) -> str:
    """
    Main function used by UI / generator engine.
    Returns full setup.sh script text.
    """

    sections = [
        _script_header(config["app_name"]),
        _project_init(config),
        _install_dependencies(config),
        _ios_pods(config),
        _native_mode_notice(config),
        _create_folders(),
        _create_stub_files(config),
        _final_instructions(config),
    ]

    return "\n".join(sections)
