# Day 5 – PlacementGPT: RAG, Tools, Memory & Agent

## Overview

PlacementGPT is an AI-powered placement preparation assistant built using Python, LangChain, Groq, ChromaDB, and LangGraph.

It uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from a placement knowledge base and generate answers to student questions.

## Features

- RAG-based knowledge retrieval using ChromaDB
- Custom search tool using LangChain
- Groq LLM integration
- Conversation memory using LangGraph's InMemorySaver
- Agent creation using LangChain's create_agent
- Placement preparation support for DBMS, OS, Computer Networks, Aptitude, and HR interviews

## Technologies Used

- Python
- LangChain
- LangChain-Groq
- LangGraph
- ChromaDB
- Groq API

## Project Structure

```text
Day-5/
├── task.py
├── requirements.txt
└── README.md
```

## Setup and Execution

1. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Set your Groq API key as an environment variable.

   PowerShell:

   ```powershell
   $env:GROQ_API_KEY="YOUR_GROQ_API_KEY"
   ```

3. Run the application:

   ```bash
   python task.py
   ```

## Knowledge Base

The current knowledge base contains information about:

- DBMS
- Operating Systems
- Computer Networks
- Aptitude
- HR Interviews

## Note

This is an educational prototype. It uses a small predefined knowledge base and in-memory conversation storage. Conversation memory is cleared when the program stops.