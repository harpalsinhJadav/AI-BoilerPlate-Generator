"""
Bash Script Generator (V2)
--------------------------
Creates runnable setup.sh including full project source code.
"""

from typing import Dict, List
from core.template_engine import generate_templates
from core.native_patch_engine import apply_native_patches


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def _join(items: List[str]) -> str:
    return " ".join(sorted(set(items))) if items else ""


def _bash_write_file(path: str, content: str) -> str:
    return f"""
mkdir -p "$(dirname '{path}')"
cat > "{path}" <<'EOF'
{content}
EOF
"""


# --------------------------------------------------
# Script sections
# --------------------------------------------------

def _header(app: str) -> str:
    return f"""#!/bin/bash
set -e

echo "🚀 Mobile AI Generator"
echo "Project: {app}"
echo "-----------------------------------"
"""


def _init_project(config: Dict) -> str:
    app = config["app_name"]

    if config["stack"] == "rn_cli":
        return f"""
echo "📱 Creating React Native CLI project..."
npx @react-native-community/cli@latest init {app}
cd {app}
"""
    else:
        return f"""
echo "📱 Creating Expo project..."
npx create-expo-app@latest {app}
cd {app}
"""


def _install_deps(config: Dict) -> str:
    deps = _join(config["dependencies"])
    dev_deps = _join(config["dev_dependencies"])

    script = '\necho "📦 Installing dependencies..."\n'

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
cd ios && pod install && cd ..
"""


def _write_templates(config: Dict) -> str:
    files = generate_templates(config)
    script = '\necho "🧩 Writing generated source files..."\n'

    for path, content in files.items():
        script += _bash_write_file(path, content)

    return script


def _final_msg(config: Dict) -> str:
    app = config["app_name"]

    return f"""
echo "-----------------------------------"
echo "✅ Project ready!"
echo ""
echo "Run the app:"
echo "cd {app}"
echo "npm start"
echo "npm run ios"
echo "npm run android"
"""


# --------------------------------------------------
# Public API
# --------------------------------------------------

def generate_bash_script(config: Dict) -> str:
    parts = [
        _header(config["app_name"]),
        _init_project(config),
        _install_deps(config),
        _write_templates(config),       # write files first
        apply_native_patches(config),   # apply native patches
        _ios_pods(config),              # pods AFTER deps, files & patches
        _final_msg(config),
    ]

    return "\n".join(parts)
