import google.generativeai as genai
import os

# 1. Configure your API key
# Replace "YOUR_GEMINI_API_KEY_HERE" with your actual key
api_key = ""
genai.configure(api_key=api_key)

print("Checking available models for your API key...\n")

try:
    # 2. List all models
    found_flash = False
    for m in genai.list_models():
        # We only care about models that generate content (chatbots)
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Available: {m.name}")
            if "gemini-1.5-flash" in m.name:
                found_flash = True

    print("\n--------------------------------------------------")
    if found_flash:
        print("🎉 GOOD NEWS: 'gemini-1.5-flash' is available!")
    else:
        print("⚠️ NOTE: 'gemini-1.5-flash' was NOT found in your list.")
        print("This likely means your API key is on an older tier or region.")
        print("Please stick with 'gemini-pro' in your code for now.")

except Exception as e:
    print(f"❌ Error fetching models: {e}")