#!/usr/bin/env python3
"""
Quick Test Script
-----------------
Verifies core functionality without running the full UI.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from ai.llm_provider import run_llm, is_llm_available, get_available_providers
        from ai.feature_inference import infer_features
        from ai.screen_inference import infer_screens
        from core.generator_engine import build_project_config
        from core.feature_registry import get_all_features
        from core.validation import sanitize_app_name, sanitize_description
        from core.native_patch_engine import apply_native_patches
        from output.bash_script_generator import generate_bash_script
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_validation():
    """Test validation layer."""
    print("\nTesting validation...")
    
    try:
        from core.validation import sanitize_app_name, sanitize_description
        
        # Test app name sanitization
        assert sanitize_app_name("My App") == "MyApp"
        assert sanitize_app_name("my-app-123") == "Myapp123"  # capitalize() lowercases rest
        assert sanitize_app_name("123app") == "App123app"
        
        # Test description sanitization
        desc = sanitize_description("App with `dangerous` $chars")
        assert "`" not in desc
        assert "$" not in desc
        
        print("✅ Validation tests passed")
        return True
    except AssertionError as e:
        print(f"❌ Validation test failed: Assertion error")
        return False
    except Exception as e:
        print(f"❌ Validation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_feature_registry():
    """Test feature registry."""
    print("\nTesting feature registry...")
    
    try:
        from core.feature_registry import get_all_features, get_default_features
        
        features = get_all_features()
        assert len(features) > 0
        
        defaults = get_default_features("rn_cli")
        assert len(defaults) > 0
        
        print(f"✅ Feature registry: {len(features)} features, {len(defaults)} defaults")
        return True
    except Exception as e:
        print(f"❌ Feature registry test failed: {e}")
        return False


def test_llm_provider():
    """Test LLM provider."""
    print("\nTesting LLM provider...")
    
    try:
        from ai.llm_provider import is_llm_available, get_available_providers
        
        providers = get_available_providers()
        
        if providers:
            print(f"✅ LLM available: {', '.join(providers)}")
        else:
            print("⚠️  No LLM providers configured (this is OK, keyword fallback will work)")
        
        return True
    except Exception as e:
        print(f"❌ LLM provider test failed: {e}")
        return False


def test_keyword_fallback():
    """Test keyword-based feature detection (no API key needed)."""
    print("\nTesting keyword fallback...")
    
    try:
        from ai.feature_inference import keyword_feature_detection
        from ai.screen_inference import keyword_screen_detection
        
        # Test feature detection
        features = keyword_feature_detection(
            "fitness app with login and notifications",
            "rn_cli"
        )
        assert "auth" in features or "navigation" in features
        
        # Test screen detection
        screens = keyword_screen_detection(
            "app with login and profile"
        )
        assert "Login" in screens or "Home" in screens
        
        print(f"✅ Keyword fallback: {len(features)} features, {len(screens)} screens")
        return True
    except Exception as e:
        print(f"❌ Keyword fallback test failed: {e}")
        return False


def test_project_generation():
    """Test full project generation."""
    print("\nTesting project generation...")
    
    try:
        from core.generator_engine import build_project_config
        from output.bash_script_generator import generate_bash_script
        
        config = build_project_config(
            app_name="TestApp",
            stack_label="React Native CLI",
            description="Simple app with login",
            automation_mode="Safe automatic + fallback (recommended)",
        )
        
        # Note: TestApp becomes Testapp due to PascalCase conversion
        assert config["app_name"] == "Testapp"
        assert config["stack"] == "rn_cli"
        assert len(config["features"]) > 0
        assert len(config["screens"]) > 0
        
        # Generate bash script
        script = generate_bash_script(config)
        assert "#!/bin/bash" in script
        assert "Testapp" in script
        
        print(f"✅ Project generation successful")
        print(f"   Features: {', '.join(config['features'][:5])}")
        print(f"   Screens: {', '.join(config['screens'])}")
        return True
    except Exception as e:
        print(f"❌ Project generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Mobile AI Boilerplate Generator - Quick Test")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_validation,
        test_feature_registry,
        test_llm_provider,
        test_keyword_fallback,
        test_project_generation,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    if all(results):
        print("\n🎉 All tests passed! System is ready.")
        print("\nNext steps:")
        print("1. (Optional) Configure API keys in .env")
        print("2. Run: streamlit run ui/app.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
