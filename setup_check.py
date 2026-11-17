"""Setup check: confirms your dev container can talk to the model.

    python setup_check.py             first time, or to check again
    python setup_check.py --new-key   replace your saved key
"""

import sys
from getpass import getpass

import openai
from dotenv import dotenv_values, set_key

MODEL = "google/gemma-4-26b-a4b-it:floor"  # change only if your instructor says so
ENV_FILE = ".env"

# What to tell you for each kind of error OpenRouter can send back
FIXES = {
    401: "The key wasn't accepted. Copy it again and run: python setup_check.py --new-key",
    402: "The key is out of credit or hit its spending limit. Class key: tell your instructor. Your own key: add credit on OpenRouter.",
    403: f"This key isn't allowed to use {MODEL}. Tell your instructor.",
    404: f"OpenRouter doesn't recognize the model {MODEL}. Tell your instructor.",
    429: "The model is busy right now. Wait a minute and run this again.",
}


def stop(message):
    print(f"❌ {message}")
    sys.exit(1)


# 1. Use the saved key, or ask for one and save it to .env
key = None if "--new-key" in sys.argv else dotenv_values(ENV_FILE).get("OPENROUTER_API_KEY")
if not key:
    print("Paste your API key and press Enter. (Nothing appears while you paste. That's normal.)")
    key = getpass("Key: ").strip()
    if not key:
        stop("No key entered. Run this again and paste the key before pressing Enter.")
    set_key(ENV_FILE, "OPENROUTER_API_KEY", key, quote_mode="never")
    print("✅ Key saved to .env. Git ignores this file, so it never gets uploaded.")
else:
    print(f"✅ Using the key saved in .env (ends in ...{key[-4:]})")

# 2. Send the model one test message
print(f"Sending a test message to {MODEL} ...")
client = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)
try:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "Reply with exactly one word: ready"}],
        max_tokens=50,
    )
except openai.APIConnectionError:
    stop("Couldn't reach OpenRouter. Check your internet connection and run this again.")
except openai.APIStatusError as error:
    stop(FIXES.get(error.status_code, f"OpenRouter returned an error. Tell your instructor: {error}"))

reply = response.choices[0].message.content
if not reply:
    stop("The model sent back an empty reply. Tell your instructor.")
print(f'✅ The model replied: "{reply.strip()}"')
print("🎉 All set! Your dev container can talk to the model.")