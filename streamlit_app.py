"""Your personal AI assistant.

Run it from the terminal:
    streamlit run app.py
"""

import os

import openai
import streamlit as st
from dotenv import load_dotenv

# ---------- Part 1: the personality ----------
# Change these to make the assistant your own.
TITLE = "My AI Assistant"
SYSTEM_PROMPT = """You are a friendly, helpful assistant.
Keep your answers short: two or three sentences."""

# ---------- Settings ----------
MODEL = "google/gemma-4-26b-a4b-it:floor"
MAX_REPLY_TOKENS = 300  # the longest reply allowed, in tokens
MAX_MESSAGES = 20  # the most messages one visitor can send in a chat

# On your Codespace, the key comes from .env. Once deployed, it comes
# from the app's secrets. Either way, it never appears in this file.
load_dotenv()
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

st.title(TITLE)

# ---------- Part 2: this chat's history ----------
# The model remembers nothing between calls, so the app keeps the whole
# conversation here and sends all of it every time.
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

messages_sent = len([m for m in st.session_state.messages if m["role"] == "user"])
if messages_sent >= MAX_MESSAGES:
    st.info("You've reached the message limit for this chat. Thanks for trying it out!")
    st.stop()

# ---------- Part 3: the call ----------
user_text = st.chat_input("Say something")
if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    st.chat_message("user").write(user_text)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            # The personality goes first, then the conversation so far
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages,
            max_tokens=MAX_REPLY_TOKENS,
        )
    except openai.APIError as error:
        st.session_state.messages.pop()  # forget the message that didn't get a reply
        st.error(f"Couldn't get a reply from the model: {error}")
        st.stop()

    reply = response.choices[0].message.content or "(The model sent back an empty reply.)"
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)