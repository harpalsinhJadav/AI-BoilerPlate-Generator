# 📱 Mobile AI Boilerplate Generator

> **AI-assisted mobile app scaffolding** → Transform app ideas into production-ready React Native projects with zero manual setup.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)
[![React Native](https://img.shields.io/badge/React_Native-Latest-61DAFB.svg)](https://reactnative.dev/)

---

## 🎯 What is This?

An **AI mobile app factory** that generates complete, runnable React Native projects from natural language descriptions. No boilerplate copy-pasting, no manual native configuration—just describe your app and get a production-ready codebase.

### Key Features

✅ **AI Feature Detection** - Semantic understanding of app requirements (Gemini/OpenAI)  
✅ **Zero Manual Native Setup** - Automated Android/iOS configuration  
✅ **Smart Fallback** - Works without API keys (keyword-based detection)  
✅ **Production Ready** - Redux, Navigation, Testing, TypeScript support  
✅ **Runnable Scripts** - One-command project generation  
✅ **Multi-LLM Support** - Gemini, OpenAI, future local models  

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    UI Layer (Streamlit)                  │
│  • Project configuration                                 │
│  • AI detection preview                                  │
│  • Feature override                                      │
│  • Bash script generation                                │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              AI Inference Layer                          │
│  • LLM Provider (centralized)                            │
│  • Feature inference (semantic + keyword)                │
│  • Screen inference (semantic + keyword)                 │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Core Engine Layer                           │
│  • Generator engine (orchestration)                      │
│  • Feature registry (catalog)                            │
│  • Screen registry (metadata)                            │
│  • Validation layer (sanitization)                       │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│           Template & Native Layer                        │
│  • Template engine (JSX/TS generation)                   │
│  • Native patch engine (Android/iOS)                     │
│  • Bash script generator (runnable output)               │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 18+** (for generated projects)
- **macOS** (for iOS development) or **Linux/Windows** (Android only)

### Installation

```bash
# Clone the repository
git clone https://github.com/harpalsinhJadav/AI-BoilerPlate-Generator.git
cd AI-BoilerPlate-Generator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup API keys (optional but recommended)
cp .env.template .env
# Edit .env and add your GOOGLE_API_KEY or OPENAI_API_KEY
```

### Run the Generator

```bash
streamlit run ui/app.py
```

Open your browser to `http://localhost:8501`

---

## 📖 Usage Guide

### 1. **Configure Your Project**

- **App Name**: `MyAwesomeApp` (no spaces, PascalCase recommended)
- **Tech Stack**: Choose between React Native CLI or Expo
- **Description**: Describe your app naturally:
  ```
  A fitness tracking app with user authentication, workout logging,
  progress charts, push notifications, and social sharing
  ```

### 2. **Run AI Detection** (Optional)

Click "Run AI Detection" to preview what features the AI will infer from your description.

### 3. **Override Features**

Manually select/deselect features as needed:
- ✅ React Navigation
- ✅ Redux Toolkit
- ✅ Authentication Flow
- ✅ Push Notifications
- ✅ Biometric Auth
- And more...

### 4. **Generate Project**

Click "🚀 Generate Project Setup" to create your bash script.

### 5. **Run the Script**

```bash
# Download the generated script
chmod +x MyAwesomeApp_setup.sh
./MyAwesomeApp_setup.sh
```

### 6. **Start Developing**

```bash
cd MyAwesomeApp
npm start

# In separate terminals:
npm run ios     # macOS only
npm run android
```

---

## 🧠 AI Capabilities

### Feature Detection

The AI understands natural language and maps it to concrete features:

| **Description** | **Detected Features** |
|---|---|
| "login and signup" | `auth`, `forms`, `navigation` |
| "push notifications" | `notifications`, native iOS/Android permissions |
| "dark mode" | `theme` |
| "multiple languages" | `i18n` |
| "biometric login" | `biometric`, `auth` |

### Screen Detection

Automatically infers required screens:

| **Description** | **Generated Screens** |
|---|---|
| "user profile" | `Home`, `Profile`, `Settings` |
| "chat app" | `Home`, `Chat`, `Login`, `Signup` |
| "e-commerce" | `Home`, `ProductList`, `Cart`, `Checkout` |

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file (copy from `.env.template`):

```bash
# Recommended: Google Gemini (free tier available)
GOOGLE_API_KEY=your_google_api_key_here

# Optional: OpenAI (for multi-LLM support)
OPENAI_API_KEY=your_openai_api_key_here
```

**Get API Keys:**
- **Gemini**: https://makersuite.google.com/app/apikey
- **OpenAI**: https://platform.openai.com/api-keys

### Without API Keys

The generator works without API keys using **keyword-based fallback**:
- Less semantic understanding
- Still generates valid projects
- Recommended for offline/testing

---

## 📦 Generated Project Structure

```
MyAwesomeApp/
├── App.js                      # Root component with Redux + Navigation
├── index.js                    # Entry point
├── src/
│   ├── screens/                # Screen components
│   │   ├── HomeScreen.js
│   │   ├── LoginScreen.js
│   │   └── ProfileScreen.js
│   ├── components/             # Reusable components
│   │   └── AppButton.js
│   ├── navigation/             # Navigation setup
│   │   └── AppNavigator.js
│   ├── store/                  # Redux store
│   │   ├── index.js
│   │   └── sampleSlice.js
│   ├── api/                    # API client (Axios)
│   │   └── client.js
│   └── theme/                  # Theme configuration
│       ├── colors.js
│       └── index.js
├── tests/                      # Jest tests
│   └── screens/
│       └── HomeScreen.test.js
├── android/                    # Native Android (auto-configured)
└── ios/                        # Native iOS (auto-configured)
```

---

## 🛠️ Native Automation

### Android Patches

Automatically applies:
- ✅ Permissions (biometric, camera, location, notifications)
- ✅ Splash screen configuration
- ✅ MainActivity updates
- ✅ Firebase setup instructions

### iOS Patches

Automatically applies:
- ✅ Info.plist permissions (Face ID, camera, location)
- ✅ AppDelegate updates
- ✅ Launch screen configuration
- ✅ Firebase setup instructions

**Zero manual Xcode/Android Studio configuration required!**

---

## 🧪 Testing

Generated projects include:
- ✅ Jest configuration
- ✅ React Test Renderer
- ✅ Screen component tests
- ✅ 100% test coverage ready

Run tests:
```bash
npm test
```

---

## 🗺️ Roadmap

### ✅ V1 (Current)
- [x] AI feature detection
- [x] AI screen detection
- [x] Keyword fallback
- [x] Native patch engine
- [x] Bash script generation
- [x] Multi-LLM support (Gemini, OpenAI)
- [x] Input validation

### 🚧 V2 (In Progress)
- [ ] **AI Code Generation** - Generate actual screen JSX/TSX
- [ ] **Redux Slice Generation** - Auto-generate state management
- [ ] **API Service Generation** - Create API client methods
- [ ] **Component Inference** - Smart component suggestions
- [ ] **TypeScript Support** - Full TS project generation
- [ ] **Expo Router** - Modern navigation for Expo

### 🔮 V3 (Future)
- [ ] **Local LLM Support** - Run without cloud APIs
- [ ] **Custom Templates** - User-defined project templates
- [ ] **CI/CD Integration** - GitHub Actions, GitLab CI
- [ ] **Database Integration** - Firebase, Supabase, MongoDB
- [ ] **Backend Generation** - Node.js/Express API scaffolding

---

## 📚 Documentation

### Core Modules

| Module | Purpose |
|---|---|
| `ai/llm_provider.py` | Centralized LLM interface (Gemini, OpenAI) |
| `ai/feature_inference.py` | Feature detection (semantic + keyword) |
| `ai/screen_inference.py` | Screen detection (semantic + keyword) |
| `core/generator_engine.py` | Main orchestration logic |
| `core/feature_registry.py` | Feature catalog with dependencies |
| `core/screen_registry.py` | Screen metadata (V2 prep) |
| `core/validation.py` | Input sanitization & validation |
| `core/template_engine.py` | Code template generation |
| `core/native_patch_engine.py` | Android/iOS automation |
| `output/bash_script_generator.py` | Runnable script creation |

### Adding New Features

1. **Update Feature Registry** (`core/feature_registry.py`):
```python
{
    "id": "my_feature",
    "label": "My Awesome Feature",
    "default": False,
    "stacks": ["rn_cli", "expo"],
    "dependencies": ["my-npm-package"],
    "dev_dependencies": [],
    "native": {
        "android": ["my_android_patch"],
        "ios": ["my_ios_patch"],
    },
    "screens": [],
    "description_keywords": ["my", "feature", "keywords"],
}
```

2. **Add Native Patches** (if needed):
- `native_rules/android/my_patch.py`
- `native_rules/ios/my_patch.py`

3. **Update Templates** (`core/template_engine.py`)

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

- **LangChain** - LLM orchestration
- **Streamlit** - Beautiful UI framework
- **React Native** - Mobile framework
- **Google Gemini** - AI inference
- **OpenAI** - Alternative LLM support

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/harpalsinhJadav/AI-BoilerPlate-Generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/harpalsinhJadav/AI-BoilerPlate-Generator/discussions)

---

**Built with ❤️ by the AI Mobile Factory Team**
