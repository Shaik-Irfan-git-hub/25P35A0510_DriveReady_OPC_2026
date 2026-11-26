# Day 4 – PlacementGPT Agent

## Overview

PlacementGPT is an AI-powered placement preparation assistant built using Python, LangChain, Groq, Pydantic, and Google Sheets.

It helps students with career guidance, skill recommendations, learning roadmaps, and placement preparation.

## Features

- AI-powered career guidance
- Career skill requirements lookup
- Predefined learning roadmaps for four career roles
- Student enquiry validation using Pydantic
- Student enquiry storage using Google Sheets
- Structured output extraction
- LangChain agent with tool calling
- Conversation history management
- Explicit consent check before saving student enquiries

## Supported Career Roles

1. AI Applied Engineer
2. Software Developer
3. Python Developer
4. Data Analyst

## Technologies Used

- Python
- Google Colab
- LangChain
- LangChain-Groq
- Groq LLM (`openai/gpt-oss-20b`)
- Pydantic
- Google Sheets API
- gspread

## Tools Implemented

1. `get_role_requirements()` – Retrieves recommended skills for a selected career role.
2. `get_learning_roadmap()` – Provides a predefined learning roadmap.
3. `log_student_enquiry()` – Validates and stores student enquiries in Google Sheets after explicit consent.

## Project Structure

```text
Day-4/
├── AgenticAI_Day4_PlacementGPT.py
└── README.md
```

## Setup Instructions

1. Open Google Colab.
2. Install the required dependencies:

   ```python
   %pip install -q langchain langchain-groq gspread pydantic
   ```

3. Add your `GROQ_API_KEY` to Google Colab Secrets.
4. Run the Python file in the Colab environment.
5. Authenticate your Google account when prompted.
6. Execute the required functions and interact with PlacementGPT.

## Example Usage

```python
response = chat(
    "I'm interested in becoming an AI Applied Engineer. "
    "What skills should I learn?"
)

print(response)
```

To generate a learning roadmap:

```python
response = chat(
    "Give me a step-by-step roadmap "
    "to become an AI Applied Engineer."
)

print(response)
```

## Google Sheets Integration

Student enquiries are stored with the following fields:

- Name
- Target Role
- Current Skills
- Goal

The saving tool requires explicit consent before storing student information.

## Important Notes

- This project is designed for Google Colab and uses Colab authentication and Secrets.
- Career requirements and roadmaps are based on predefined sample data.
- The project does not fetch live job-market requirements.
- Completing a roadmap does not guarantee placement.
- Keep API keys and credentials private.

## Future Improvements

- Add more career roles.
- Integrate live job-market information.
- Add resume analysis.
- Add aptitude and coding assessment modules.
- Build a web-based interface.
- Add personalized progress tracking.

## Author

Shaik Irfan Sharieff