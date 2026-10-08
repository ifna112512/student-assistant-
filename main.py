import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent
load_dotenv()
students = {
    "101": {
        "name": "Arun",
        "department": "CSE",
        "attendance": 82
    },
    "102": {
        "name": "Priya",
        "department": "AI",
        "attendance": 91
    }
}
@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)
        return str(result)
    except Exception:
        return "Sorry, I could not calculate that expression."
@tool
def get_student_info(name: str) -> str:
    """Get the department of a student."""
    for student in students.values():
        if student["name"].lower() == name.lower():
            return (
                f"{student['name']} is from "
                f"the {student['department']} department."
            )
    return f"I couldn't find {name} in the student database."
@tool
def get_attendance(name: str) -> str:
    """Get a student's attendance percentage."""
    for student in students.values():
        if student["name"].lower() == name.lower():
            return (
                f"{student['name']}'s attendance is "
                f"{student['attendance']}%."
            )
    return f"I couldn't find {name} in the student database."
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)
tools = [
    calculator,
    get_student_info,
    get_attendance
]
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
You are a helpful Student Assistant Agent.

You have three tools:

1. calculator
   Use this for mathematical calculations.

2. get_student_info
   Use this when the user asks about a student's department.

3. get_attendance
   Use this when the user asks about a student's attendance.

For general questions, answer directly without using student tools.

Choose the appropriate tool automatically based on the user's request.
Do not invent student information.
If a student is not found, clearly say that the student is not in the database.
"""
)
def main():
    print("=" * 50)
    print("       STUDENT ASSISTANT AGENT")
    print("=" * 50)
    print("Type 'exit' to stop the program.")
    print()
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Agent: Goodbye!")
            break
        try:
            response = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_input
                        }
                    ]
                }
            )
            final_answer = response["messages"][-1].content
            print("Agent:", final_answer)
            print()
        except Exception as e:
            print("Agent: Sorry, something went wrong.")
            print("Error:", e)
            print()
if __name__ == "__main__":
    main()