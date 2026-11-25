# Day 2 – PlacementGPT Chatbot

## Overview
Developed an interactive AI-powered placement assistance chatbot using Python and Groq API.

## Features
- Placement preparation guidance
- Resume building assistance
- Interview question generation
- Aptitude practice support
- Career guidance and learning roadmaps
- Conversation history and contextual responses
- Interactive command-line interface
- Exit commands: bye, exit, quit

## Implementation
- Integrated Groq API using the Groq Python SDK.
- Used the `openai/gpt-oss-120b` model.
- Designed a system prompt to define the chatbot's role and behavior.
- Maintained conversation history using a Python list.
- Limited the context to the latest 10 conversation exchanges.

## Technologies Used
- Python
- Groq API
- Large Language Models (LLMs)
- JSON
- Environment Variables

## Execution

Install the dependency:

```bash
pip install groq
```

Run the application:

```bash
python task.py
```

## API Security
The Groq API key is accessed through the `GROQ_API_KEY` environment variable. No API credentials are stored in the source code.