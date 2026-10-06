#!/usr/bin/env python3
import os
import sys

def colored(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def main():
    print(colored("================================================================", "1;36"))
    print(colored("                 AURA-AGI Configuration Wizard                  ", "1;36"))
    print(colored("================================================================", "1;36"))
    print("\nThis wizard will help you set up your API keys and configuration.")
    print("Press Enter to skip any key (it will remain empty or keep its current value).\n")

    env_path = ".env"
    env_data = {}

    # Read existing .env if it exists
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    key, val = line.strip().split("=", 1)
                    env_data[key] = val

    def prompt_key(key, description, default_val=""):
        current = env_data.get(key, default_val)
        current_display = f" (Current: {current[:5]}...)" if current and len(current) > 5 else ""
        print(colored(f"\n[?] {description}", "1;33"))
        print(f"    Key: {key}{current_display}")
        try:
            val = input("    -> ")
        except (KeyboardInterrupt, EOFError):
            print("\nSetup cancelled.")
            sys.exit(1)
        
        if val.strip():
            env_data[key] = val.strip()
        elif current:
            env_data[key] = current

    import secrets
    if "API_SECRET" not in env_data or not env_data["API_SECRET"]:
        env_data["API_SECRET"] = secrets.token_hex(32)
        print(colored("\n[i] Generated new API_SECRET for the Kiosk server.", "1;32"))

    # Core Keys
    prompt_key("GROQ_AI", "Groq API Key (Required for fast text generation)")
    prompt_key("OPENROUTER", "OpenRouter API Key (Fallback and main chat provider)")
    prompt_key("DEEPINFRA", "DeepInfra API Key (Vision & fallback chat)")
    prompt_key("HUGGING_FACE_READ", "HuggingFace Read Token (Fallback chat)")

    # Optional Keys
    prompt_key("DECOHERE_AI", "Decohere API Key (Image Generation)")
    prompt_key("WEATHER_API", "Weather API Key (from weatherapi.com)")
    prompt_key("SERPER_API_KEY", "Serper API Key (for Google Search tool)")

    # Preferences
    prompt_key("AURA_STT", "Speech-to-Text Engine ('auto', 'vosk', 'whisper', 'browser')", default_val="auto")
    prompt_key("AURA_MIC_INDEX", "Microphone Device Index (default -1)", default_val="-1")

    # Save logic
    print(colored("\nSaving configuration...", "1;32"))
    with open(env_path, "w", encoding="utf-8") as f:
        for k, v in env_data.items():
            f.write(f"{k}={v}\n")
    
    print(colored(f"\nConfiguration saved to {os.path.abspath(env_path)}!", "1;32"))
    print("You can run this wizard again anytime by running: python configure.py")
    print(colored("================================================================", "1;36"))

if __name__ == "__main__":
    main()
