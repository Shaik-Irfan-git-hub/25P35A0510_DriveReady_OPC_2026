
# ==========================================
# PlacementGPT - Day 5
# RAG + Tools + Memory + Agent
# ==========================================

# ------------------------------
# IMPORTS
# ------------------------------

import os
import chromadb

from langchain.tools import tool
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent


# ------------------------------
# GROQ API KEY
# ------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. "
        "Set it as an environment variable before running."
    )

print("Groq API loaded successfully!")


# ------------------------------
# PLACEMENT KNOWLEDGE BASE
# ------------------------------

PLACEMENT_KNOWLEDGE = {

    "dbms": """
DBMS stands for Database Management System.

Primary Key:
A unique identifier for each record in a table.

Foreign Key:
A column used to establish relationships between tables.

Normalization:
The process of reducing data redundancy
and improving data integrity.
""",

    "os": """
Operating System acts as an interface
between the user and computer hardware.

Main Functions:
- Process Management
- Memory Management
- File Management

CPU Scheduling Algorithms:
- FCFS
- SJF
- Round Robin
""",

    "cn": """
Computer Networks connect computers and devices.

OSI Model Layers:
1. Physical
2. Data Link
3. Network
4. Transport
5. Session
6. Presentation
7. Application

Common Protocols:
- TCP
- UDP
- HTTP
- HTTPS
""",

    "aptitude": """
Important Aptitude Topics:

- Percentages
- Profit and Loss
- Time and Work
- Probability
- Time and Distance
""",

    "hr": """
Common HR Interview Questions:

- Tell me about yourself.
- Why should we hire you?
- What are your strengths?
- What are your weaknesses?
"""
}

print("Placement knowledge base loaded!")


# ------------------------------
# CHROMADB SETUP
# ------------------------------

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="placementgpt_knowledge"
)

# Insert or update knowledge base documents
collection.upsert(
    ids=list(PLACEMENT_KNOWLEDGE.keys()),
    documents=list(PLACEMENT_KNOWLEDGE.values())
)

print(
    f"ChromaDB ready! Documents: {collection.count()}"
)


# ------------------------------
# SEARCH TOOL
# ------------------------------

@tool
def search_knowledge(question: str) -> str:
    """
    Search the PlacementGPT knowledge base
    for relevant placement preparation information.
    """

    if not question.strip():
        return "Please provide a valid question."

    if collection.count() == 0:
        return "The knowledge base is empty."

    results = collection.query(
        query_texts=[question],
        n_results=1
    )

    documents = results.get("documents", [[]])
    ids = results.get("ids", [[]])

    if not documents or not documents[0]:
        return "No relevant information was found."

    document = documents[0][0]
    topic = ids[0][0] if ids and ids[0] else "unknown"

    return (
        f"Best matching topic: {topic}\n\n"
        f"Knowledge:\n{document}"
    )


print("\nDEBUG: Testing CN retrieval directly")

print(
    search_knowledge.invoke({
        "question": "Explain the OSI model and its seven layers"
    })
)


# ------------------------------
# MEMORY
# ------------------------------

memory = InMemorySaver()

print("Conversation memory initialized!")


# ------------------------------
# LLM
# ------------------------------

llm = ChatGroq(
    model=os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b"
    ),
    api_key=GROQ_API_KEY,
    temperature=0
)

print("Groq LLM initialized!")


# ------------------------------
# SYSTEM PROMPT
# ------------------------------

SYSTEM = """
You are PlacementGPT,
an AI Placement Preparation Assistant.

You help students prepare for:

1. Aptitude
2. DBMS
3. Operating Systems
4. Computer Networks
5. HR Interviews

RULES:

- For DBMS, OS, CN, Aptitude and HR questions,
  use the search_knowledge tool first.

- Check whether the retrieved information is
  actually relevant to the user's question.

- Do not present unrelated retrieved information
  as an answer.

- If the knowledge base does not contain relevant
  information, clearly say:
  "I could not find relevant information
  in my knowledge base."

- Answer in simple, beginner-friendly language.

- Keep technical explanations interview-friendly.

- Remember personal details shared by the user
  during the current conversation.

- Do not invent facts.
"""


# ------------------------------
# AGENT
# ------------------------------

agent = create_agent(
    model=llm,
    tools=[search_knowledge],
    system_prompt=SYSTEM,
    checkpointer=memory
)

print("PlacementGPT agent created successfully!")


# ------------------------------
# THREAD CONFIGURATION
# ------------------------------

config = {
    "configurable": {
        "thread_id": "placementgpt-session-1"
    }
}


# ------------------------------
# CHAT FUNCTION
# ------------------------------

def ask(question: str) -> str:
    """
    Send a question to PlacementGPT
    and return the assistant's response.
    """

    if not question.strip():
        return "Please enter a question."

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },
        config=config
    )

    messages = result.get("messages", [])

    if not messages:
        return "No response received from the agent."

    response = messages[-1].content

    # Handle both string and block-based responses
    if isinstance(response, str):
        return response

    if isinstance(response, list):
        text_parts = []

        for block in response:
            if isinstance(block, dict) and "text" in block:
                text_parts.append(block["text"])

        return "\n".join(text_parts)

    return str(response)


# ------------------------------
# TESTS
# ------------------------------

if __name__ == "__main__":

    print("\n================================")
    print("      PLACEMENTGPT TESTING")
    print("================================")

    # Test 1: RAG + Tool Calling
    print("\nTEST 1: DBMS Knowledge Retrieval")

    print(
        ask("What is normalization in DBMS?")
    )

    print("\n--------------------------------")

    # Test 2: Conversation Memory
    print("\nTEST 2: Conversation Memory")

    print(
        ask("My name is Irfan. Remember it.")
    )

    print(
        "Memory Test:",
        ask("What is my name?")
    )

    print("\n--------------------------------")

    # Test 3: OS Knowledge Retrieval
    print("\nTEST 3: Operating System")

    print(
        ask("What are OS scheduling algorithms?")
    )

    print("\n--------------------------------")

    # Test 4: Another Knowledge Base Topic
    print("\nTEST 4: Computer Networks")

    print(
        ask("Explain the OSI model.")
    )

    print("\n================================")
    print("       TESTING COMPLETED")
    print("================================")
