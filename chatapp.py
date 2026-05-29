import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
import os
import json

#GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
# Where memory is saved
MEMORY_FILE = "C:\\Users\\Amiya\\memory.json"

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=st.secrets["GROQ_API_KEY"])

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_memory(messages):
    with open(MEMORY_FILE, "w") as f:
        json.dump(messages, f)

st.title("My AI Dropshipping Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = load_memory()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    save_memory(st.session_state.messages)

    with st.chat_message("user"):
        st.write(user_input)

    history = []
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            history.append(HumanMessage(content=msg["content"]))
        else:
            history.append(AIMessage(content=msg["content"]))

    response = llm.invoke(history)

    st.session_state.messages.append({
        "role": "assistant", 
        "content": response.content
    })
    save_memory(st.session_state.messages)

    with st.chat_message("assistant"):
        st.write(response.content)

if st.button("Clear Memory"):
    st.session_state.messages = []
    save_memory([])
    st.rerun()
        
