
import os
import csv
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_agent


# Get the Day-3 folder location
BASE_DIR = Path(__file__).resolve().parent

# API key must be configured in Windows environment variables
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is missing. Set it in your environment variables."
    )


# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    google_api_key=API_KEY,
    temperature=0.3
)


# System instructions
SYSTEM = """
ROLE:
You are PlacementGPT.

FACTS:
You help students with:
- Aptitude Preparation
- Coding Interviews
- HR Interviews
- Resume Building
- Career Guidance
- Roadmap Generation

RULES:
- Be professional.
- Be student friendly.
- Give practical advice.
- Use bullet points when helpful.
- Keep responses concise.

FORMAT:
Use markdown.
"""


# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    MessagesPlaceholder("history"),
    ("human", "{question}")
])


# Create LangChain chain
chain = prompt | llm | StrOutputParser()


# Conversation history
history = []


def ask(question: str) -> str:
    answer = chain.invoke({
        "history": history,
        "question": question
    })

    history.extend([
        HumanMessage(content=question),
        AIMessage(content=answer)
    ])

    return answer


# CSV-based testing
def run_tests(path=None):

    if path is None:
        path = BASE_DIR / "test.csv"

    path = Path(path)

    if not path.exists():
        print(f"Test file not found: {path}")
        return

    with open(path, "r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        print("No test cases found.")
        return

    passed = 0

    for row in rows:

        answer = chain.invoke({
            "history": [],
            "question": row["question"]
        })

        expected = row["must_include"].strip().lower()

        ok = expected in answer.lower()

        if ok:
            passed += 1

        print(
            "PASS" if ok else "FAIL",
            "|",
            row["question"],
            "→",
            answer[:70]
        )

    total = len(rows)

    print(
        f"\n{passed}/{total} tests passed ({passed / total:.0%})"
    )


# Create LangChain agent
agent = create_agent(
    model=llm,
    tools=[],
    system_prompt=SYSTEM
)


def main():

    print("\n--- PlacementGPT: Conversation Memory ---")

    print(ask(
        "Hi, my name is Irfan. I want to become a Data Scientist."
    ))

    print(ask("What career do I want to pursue?"))

    print("\n--- PlacementGPT: CSV Tests ---")
    run_tests()

    print("\n--- PlacementGPT: Agent ---")

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "How can I prepare for placements?"
            }
        ]
    })

    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
