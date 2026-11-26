import csv
import os
from typing import List

import gspread
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq
from pydantic import BaseModel, ConfigDict, Field, ValidationError

# ============================================================
# 1. CONFIGURATION AND CONNECTIONS
# ============================================================

GROQ_MODEL = "openai/gpt-oss-20b"
SHEET_NAME = "PlacementGPT Student Enquiries"

if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY not found in environment variables.")

# ChatGroq automatically reads GROQ_API_KEY from the environment
llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0.2,
    max_retries=3
)

print("Groq Connected!")


# ============================================================
# 2. GOOGLE SHEETS CONNECTION (WITH LOCAL CSV FALLBACK)
# ============================================================

class LocalCSVSheet:
    """Fallback storage if credentials.json is not present locally."""
    def __init__(self, filename="placement_enquiries.csv"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["name", "target_role", "current_skills", "goal"])

    def append_row(self, row):
        with open(self.filename, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(row)


def connect_google_sheet():
    if os.path.exists("credentials.json"):
        google_client = gspread.service_account(filename="credentials.json")
        try:
            spreadsheet = google_client.open(SHEET_NAME)
        except gspread.SpreadsheetNotFound:
            spreadsheet = google_client.create(SHEET_NAME)

        worksheet = spreadsheet.sheet1
        if not worksheet.get_all_values():
            worksheet.append_row(["name", "target_role", "current_skills", "goal"])

        print("Google Sheets Connected! URL:", spreadsheet.url)
        return worksheet

    print("credentials.json not found — using local 'placement_enquiries.csv' instead.")
    return LocalCSVSheet()


ws = connect_google_sheet()

# ============================================================
# 3. CAREER REQUIREMENTS
# ============================================================

ROLE_REQUIREMENTS = {

    "ai applied engineer": [
        "Python",
        "OOP",
        "DSA",
        "Machine Learning basics",
        "LLMs",
        "Prompt Engineering",
        "LangChain",
        "RAG",
        "APIs",
        "Database fundamentals"
    ],

    "software developer": [
        "Java or Python",
        "OOP",
        "DSA",
        "DBMS",
        "Operating Systems",
        "Computer Networks",
        "Problem Solving",
        "Git and GitHub"
    ],

    "python developer": [
        "Python",
        "OOP",
        "Data Structures",
        "File Handling",
        "Exception Handling",
        "FastAPI or Django",
        "SQL",
        "Git"
    ],

    "data analyst": [
        "Python",
        "SQL",
        "Excel",
        "Statistics",
        "Pandas",
        "NumPy",
        "Power BI",
        "Data Visualization"
    ]
}


# ============================================================
# 4. LEARNING ROADMAPS
# ============================================================

ROADMAPS = {

    "ai applied engineer": [
        "Stage 1: Python, OOP and DSA",
        "Stage 2: NumPy, Pandas and ML fundamentals",
        "Stage 3: LLMs and Prompt Engineering",
        "Stage 4: LangChain and AI Agents",
        "Stage 5: RAG and Vector Databases",
        "Stage 6: Build and deploy AI projects"
    ],

    "software developer": [
        "Stage 1: Master Java or Python",
        "Stage 2: DSA and Problem Solving",
        "Stage 3: DBMS, OS and Computer Networks",
        "Stage 4: Backend and API development",
        "Stage 5: Build full-stack projects",
        "Stage 6: Interview preparation"
    ],

    "python developer": [
        "Stage 1: Python fundamentals",
        "Stage 2: OOP and advanced Python",
        "Stage 3: File handling and databases",
        "Stage 4: FastAPI or Django",
        "Stage 5: Build backend projects",
        "Stage 6: Deployment and interviews"
    ],

    "data analyst": [
        "Stage 1: Excel and Statistics",
        "Stage 2: SQL",
        "Stage 3: Python fundamentals",
        "Stage 4: Pandas and NumPy",
        "Stage 5: Power BI and visualization",
        "Stage 6: Build data analysis projects"
    ]
}

print("Career data loaded successfully!")


# ============================================================
# 5. PYDANTIC MODEL
# ============================================================

class StudentEnquiry(BaseModel):
    """Validate student career guidance information."""

    name: str = Field(
        description="Student's name",
        min_length=2
    )

    target_role: str = Field(
        description="Student's desired career role",
        min_length=2
    )

    current_skills: str = Field(
        description="Skills currently known by the student",
        min_length=2
    )

    goal: str = Field(
        description="Student's career or placement goal",
        min_length=5
    )


print("Pydantic model created!")


# ============================================================
# 6. LANGCHAIN TOOLS
# ============================================================

@tool
def get_role_requirements(role: str) -> str:
    """
    Get recommended skills and technologies for a career role.

    Args:
        role: AI Applied Engineer, Software Developer,
              Python Developer, or Data Analyst.
    """

    role = role.lower().strip()

    requirements = ROLE_REQUIREMENTS.get(role)

    if requirements is None:
        available_roles = ", ".join(
            role.title() for role in ROLE_REQUIREMENTS
        )

        return (
            f"Role '{role}' not found. "
            f"Available roles: {available_roles}"
        )

    return (
        f"Recommended skills for {role.title()}:\n"
        + "\n".join(f"- {skill}" for skill in requirements)
    )


@tool
def get_learning_roadmap(role: str) -> str:
    """
    Get a step-by-step learning roadmap for a career role.

    Args:
        role: Desired career role.
    """

    role = role.lower().strip()

    roadmap = ROADMAPS.get(role)

    if roadmap is None:
        available_roles = ", ".join(
            role.title() for role in ROADMAPS
        )

        return (
            f"No predefined roadmap for {role}. "
            f"Available roles: {available_roles}"
        )

    return (
        f"Learning Roadmap for {role.title()}:\n"
        + "\n".join(roadmap)
    )


@tool
def log_student_enquiry(
    name: str,
    target_role: str,
    current_skills: str,
    goal: str,
    consent: bool = False
) -> str:
    """
    Save a student's enquiry to Google Sheets.

    Use this tool only after the student explicitly agrees
    to save their information.

    Args:
        name: Student's name.
        target_role: Desired career role.
        current_skills: Student's current skills.
        goal: Student's career goal.
        consent: True only when the student explicitly agrees.
    """

    if consent is not True:
        return (
            "Enquiry not saved. Explicit student consent is required."
        )

    try:
        student = StudentEnquiry(
            name=name,
            target_role=target_role,
            current_skills=current_skills,
            goal=goal
        )

        ws.append_row([
            student.name,
            student.target_role,
            student.current_skills,
            student.goal
        ])

        return (
            f"Enquiry successfully saved for {student.name}!"
        )

    except ValidationError as error:
        return f"Invalid student details: {error}"

    except Exception as error:
        return f"Unable to save enquiry: {error}"


# ============================================================
# 7. PLACEMENTGPT SYSTEM PROMPT
# ============================================================

SYSTEM = """
ROLE:
You are PlacementGPT, an AI-powered placement preparation assistant.

RESPONSIBILITIES:
Help students with:
- Aptitude Preparation
- Coding Interviews
- HR Interviews
- Resume Building
- Career Guidance
- Learning Roadmap Generation

RULES:
- Be professional and student friendly.
- Give practical advice.
- Use bullet points when helpful.
- Keep responses concise.
- Use get_role_requirements for predefined career skill requirements.
- Use get_learning_roadmap for predefined learning roadmaps.
- Never invent information from the predefined career data.
- Ask for missing information when necessary.
- Never save student information without explicit permission.
- Call log_student_enquiry only after the student explicitly agrees
  and provides all four required details.
- Pass consent=True only when that explicit agreement is present.

ADDITIONAL RULES:
- Customize roadmaps according to the student's current skills.
- Consider the student's academic year and available preparation time.
- Divide roadmaps into realistic monthly milestones when requested.
- Do not overload beginners with advanced technologies.
- Prioritize practical projects over unnecessary theory.
- Recommend DSA practice throughout preparation.
- Do not recommend fine-tuning LLMs unless there is a clear reason.
- Distinguish essential skills from optional skills.
- Start resume preparation and job applications early.
- Never claim that completing a roadmap guarantees placement.
- Clearly distinguish predefined tool data from additional suggestions.

FORMAT:
Use Markdown.
"""


# ============================================================
# 8. CREATE PLACEMENTGPT AGENT
# ============================================================

tools = [
    get_role_requirements,
    get_learning_roadmap,
    log_student_enquiry
]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM
)

print("PlacementGPT Agent Created Successfully!")


# ============================================================
# 9. CONVERSATION HISTORY AND CHAT FUNCTION
# ============================================================

history: List = []


def chat(user_text: str) -> str:
    """
    Send a message to PlacementGPT and maintain conversation history.
    """

    global history

    try:
        result = agent.invoke({
            "messages": history + [
                {"role": "user", "content": user_text}
            ]
        })

        history = result["messages"]

        last_message = history[-1]
        response = last_message.content

        if isinstance(response, str):
            return response

        return str(response)

    except Exception as error:
        print("Agent Error:", error)
        return (
            "Sorry, something went wrong. "
            "Please check the connection and try again."
        )


# ============================================================
# 10. STRUCTURED OUTPUT EXTRACTION
# ============================================================

def extract_student_details(text: str):
    """
    Extract structured student information using Pydantic.
    """

    extractor = llm.with_structured_output(StudentEnquiry)

    try:
        student = extractor.invoke(
            f"""
            Extract the following student information.

            {text}

            Return all four fields with meaningful values.
            Do not use question marks or empty values.
            """
        )

        print("\nStructured Student Details")
        print("--------------------------")
        print("Name:", student.name)
        print("Target Role:", student.target_role)
        print("Current Skills:", student.current_skills)
        print("Goal:", student.goal)

        return student

    except (ValidationError, Exception) as error:
        print("Structured Output Error:", error)
        return None


# ============================================================
# 11. SAFE TESTS
# ============================================================

def run_tests():
    """Run basic tests without saving any real student enquiry."""

    print("\nTEST 1: Career Requirements")
    print(get_role_requirements.invoke({
        "role": "AI Applied Engineer"
    }))

    print("\nTEST 2: Learning Roadmap")
    print(get_learning_roadmap.invoke({
        "role": "AI Applied Engineer"
    }))

    print("\nTEST 3: Unsupported Role")
    print(get_role_requirements.invoke({
        "role": "Pilot"
    }))

    print("\nTEST 4: Consent Protection")
    print(log_student_enquiry.invoke({
        "name": "Irfan",
        "target_role": "AI Applied Engineer",
        "current_skills": "Python, Java, DSA",
        "goal": "Prepare for AI engineering placements",
        "consent": False
    }))

    print("\nTEST 5: Pydantic Validation")

    try:
        StudentEnquiry(
            name="",
            target_role="Python Developer",
            current_skills="Python",
            goal="Get a software job"
        )

    except ValidationError as error:
        print("Validation Error:")
        print(error)

    print("\nBasic tests completed.")


# ============================================================
# 12. AGENT EXECUTION EXAMPLE
# ============================================================

if __name__ == "__main__":

    print("\n===================================")
    print("       PLACEMENTGPT READY")
    print("===================================")

    # Run safe tool and validation tests.
    run_tests()

    # Example agent interaction:
    #
    # response = chat(
    #     "I'm interested in becoming an AI Applied Engineer. "
    #     "What skills should I learn?"
    # )
    # print(response)

    # Example roadmap request:
    #
    # response = chat(
    #     "Give me a step-by-step roadmap "
    #     "to become an AI Applied Engineer."
    # )
    # print(response)

    # Example structured output:
    #
    # extract_student_details(
    #     "Name: Ravi. Target Role: Software Developer. "
    #     "Current Skills: Python, Java and basic DSA. "
    #     "Goal: Get placed as a software developer."
    # )

    print("\nPlacementGPT initialization completed.")
