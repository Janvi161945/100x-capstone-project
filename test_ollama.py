"""
Simple test script to verify Ollama setup
Run this to check if Ollama is working correctly
"""

import sys
import json


def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    print("=" * 60)
    print("TEST 1: Ollama Connection")
    print("=" * 60)

    try:
        import requests
        response = requests.get("http://localhost:11434/api/version", timeout=5)

        if response.status_code == 200:
            version = response.json().get("version", "unknown")
            print(f"✅ Ollama is running (version: {version})")
            return True
        else:
            print(f"❌ Ollama responded with status {response.status_code}")
            return False

    except ImportError:
        print("❌ 'requests' library not installed")
        print("   Run: pip install requests")
        return False

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Ollama")
        print()
        print("Quick Fix:")
        print("  1. Install Ollama: https://ollama.com")
        print("  2. Start Ollama: ollama serve")
        print()
        return False

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_model_available():
    """Test if required model is available"""
    print()
    print("=" * 60)
    print("TEST 2: Model Availability")
    print("=" * 60)

    try:
        import requests

        # Try to list models (Ollama API endpoint)
        response = requests.get("http://localhost:11434/api/tags", timeout=5)

        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])

            if not models:
                print("❌ No models installed")
                print()
                print("Install a model:")
                print("  ollama pull llama3.2")
                print()
                return False

            print("✅ Available models:")
            for model in models:
                name = model.get("name", "unknown")
                size_gb = model.get("size", 0) / (1024**3)
                print(f"   - {name} ({size_gb:.1f} GB)")

            # Check if llama3.2 is available
            model_names = [m.get("name", "") for m in models]
            if any("llama3.2" in name for name in model_names):
                print()
                print("✅ Recommended model (llama3.2) is installed")
                return True
            else:
                print()
                print("⚠️  Recommended model (llama3.2) not found")
                print("   Install it: ollama pull llama3.2")
                return True  # Still pass if other models exist

        else:
            print(f"❌ Could not list models (status {response.status_code})")
            return False

    except Exception as e:
        print(f"❌ Error checking models: {e}")
        return False


def test_simple_generation():
    """Test simple text generation"""
    print()
    print("=" * 60)
    print("TEST 3: Simple Generation")
    print("=" * 60)

    try:
        import requests

        payload = {
            "model": "llama3.2",
            "prompt": "Say only the word 'hello' and nothing else.",
            "stream": False,
            "temperature": 0
        }

        print("Sending test prompt to Ollama...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            generated_text = result.get("response", "").strip()
            print(f"✅ Ollama responded: '{generated_text}'")
            return True
        else:
            print(f"❌ Generation failed (status {response.status_code})")
            print(f"   Response: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("❌ Request timed out (Ollama might be slow)")
        print("   This is normal for first-time model loading")
        print("   Try again in a few seconds")
        return False

    except Exception as e:
        print(f"❌ Generation error: {e}")
        return False


def test_planner_import():
    """Test if planner modules can be imported"""
    print()
    print("=" * 60)
    print("TEST 4: Planner Import")
    print("=" * 60)

    try:
        from ollama_planner import OllamaClient, OllamaLearningPlanner
        print("✅ ollama_planner module imported successfully")

        from prompt_templates import get_step1_prompt
        print("✅ prompt_templates module imported successfully")

        from llm_response_schemas import validate_llm_response
        print("✅ llm_response_schemas module imported successfully")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print()
        print("Make sure you're in the right directory:")
        print("  cd /home/janvi/capstone-project")
        return False


def test_planner_basic():
    """Test basic planner functionality"""
    print()
    print("=" * 60)
    print("TEST 5: Basic Planner Test")
    print("=" * 60)

    try:
        from ollama_planner import OllamaClient, OllamaLearningPlanner

        print("Initializing planner...")
        client = OllamaClient(model="llama3.2")
        planner = OllamaLearningPlanner(client)

        print("Generating background question (this may take 10-30 seconds)...")
        question = planner.get_background_question()

        print("✅ Response received:")
        print(json.dumps(question, indent=2))

        # Basic validation
        if "question_id" in question and "question_text" in question and "options" in question:
            print()
            print("✅ Response has correct structure")
            return True
        else:
            print()
            print("⚠️  Response structure might be incorrect")
            return False

    except Exception as e:
        print(f"❌ Planner test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print()
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "OLLAMA SETUP VERIFICATION" + " " * 17 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    results = []

    # Run tests
    results.append(("Ollama Connection", test_ollama_connection()))
    results.append(("Model Availability", test_model_available()))
    results.append(("Simple Generation", test_simple_generation()))
    results.append(("Planner Import", test_planner_import()))

    # Only run planner test if previous tests passed
    if all(r[1] for r in results):
        results.append(("Basic Planner", test_planner_basic()))

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    print()

    if all(r[1] for r in results):
        print("╔" + "=" * 58 + "╗")
        print("║" + " " * 10 + "🎉 ALL TESTS PASSED! YOU'RE READY! 🎉" + " " * 10 + "║")
        print("╚" + "=" * 58 + "╝")
        print()
        print("Next steps:")
        print("  1. Run full planner test: python3 ollama_planner.py")
        print("  2. Start API server: python3 api_ollama_example.py")
        print("  3. Visit: http://localhost:8000/docs")
        print()
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print()
        print("Common fixes:")
        print("  1. Start Ollama: ollama serve")
        print("  2. Pull model: ollama pull llama3.2")
        print("  3. Install deps: pip install requests pydantic")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
