
import os
from groq import Groq

# Check API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("Please configure GROQ_API_KEY.")

# Initialize Groq client
client = Groq(api_key=api_key)

print("Groq Connected!")

MODEL = "openai/gpt-oss-120b"

SYSTEM = """
You are PlacementGPT.

Your job is to help students with:

- Placement Preparation
- Resume Building
- Interview Questions
- Aptitude Practice
- Career Guidance
- Roadmaps

Rules:
- Be friendly.
- Give concise answers.
- If asked for interview questions, provide them.
- If asked for career advice, provide step-by-step guidance.
- Encourage learning.
"""

# Conversation history
history = [
    {
        "role": "system",
        "content": SYSTEM
    }
]

MAX_TURNS = 10


def chat(user_text):

    history.append({
        "role": "user",
        "content": user_text
    })

    # Keep recent conversation history
    recent = [history[0]] + history[1:][-MAX_TURNS * 2:]

    response = client.chat.completions.create(
        model=MODEL,
        messages=recent,
        temperature=0.5
    )

    reply = response.choices[0].message.content

    history.append({
        "role": "assistant",
        "content": reply
    })

    return reply


# Initial chatbot test
print("\nPlacementGPT:")
print(chat("I am a CSE student. Tell me career options."))


# Interactive chatbot
while True:

    text = input("\nYou: ")

    if text.lower().strip() in ["bye", "exit", "quit"]:
        print("PlacementGPT: Goodbye!")
        break

    print("\nPlacementGPT:", chat(text))
