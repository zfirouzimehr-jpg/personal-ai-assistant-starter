"""Your first call to a language model.

Run it from the terminal:
    python first_call.py
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

MODEL = "google/gemma-4-26b-a4b-it:floor"

# Read your key from the .env file, then connect to OpenRouter with it.
# The key never appears in this file.
load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

# The conversation is a list of messages. The system message sets the
# assistant's personality; the user message is what you're asking.
messages = [
    {"role": "system", "content": "You are a grumpy pirate. Answer in one or two sentences."},
    {"role": "user", "content": "What's the best way to learn to code?"},
]

response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    max_tokens=200,  # the most the reply can be, measured in tokens
)

print(response.choices[0].message.content)

# Want to see everything that came back, not just the reply?
# Remove the # from the line below and run the file again.
# print(response.model_dump_json(indent=2))