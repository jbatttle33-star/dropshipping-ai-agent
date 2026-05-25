from langchain_groq import ChatGroq
from langchain_core.tools import tool
import os
import datetime

os.environ["GROQ_API_KEY"] = "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"

llm = ChatGroq(model="llama-3.3-70b-versatile")

@tool
def get_current_date() -> str:
    """Returns todays date"""
    return datetime.datetime.now().strftime("%A, %B %d %Y")

@tool
def do_math(expression: str) -> str:
    """Solves a math problem"""
    return str(eval(expression))

llm_with_tools = llm.bind_tools([get_current_date, do_math])

tasks = [
    "What is todays date?",
    "What is 1523 multiplied by 47?",
]

print("Starting AI loop...\n")
for task in tasks:
    print(f"Task: {task}")
    result = llm_with_tools.invoke(task)
    print(f"Result: {result.content}\n")

print("All tasks done!")