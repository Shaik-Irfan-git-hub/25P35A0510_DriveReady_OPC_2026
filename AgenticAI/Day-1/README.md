# Day 1 – Agentic AI

## Overview
Developed an AI-powered college assistant using LangChain and Groq LLMs. Also explored prompt injection detection using Meta's Prompt Guard model.

## Tasks Implemented

### 1. College Assistant
- Integrated Groq LLM using LangChain.
- Configured the `openai/gpt-oss-120b` model.
- Created a system prompt with predefined college information.
- Implemented rules to prevent the model from inventing unavailable information.
- Restricted responses to fewer than 80 words.

### 2. Prompt Guard
- Integrated the Groq Python SDK.
- Used the `meta-llama/llama-prompt-guard-2-22m` model.
- Tested a potential prompt injection attempt.
- Observed the model's detection score.

## Technologies Used
- Python
- LangChain
- LangChain-Groq
- Groq API
- LLMs
- Prompt Guard

## Execution
Run the program using:

```bash
python task.py
```

## Security
The Groq API key is configured through an environment variable (`GROQ_API_KEY`). No API credentials are stored in the source code.