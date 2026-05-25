import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
import os

os.environ["GROQ_API_KEY"] = "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"

llm = ChatGroq(model="llama-3.3-70b-versatile")

st.title("My AI Chat App")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    response = llm.invoke([HumanMessage(content=user_input)])

    st.session_state.messages.append({"role": "assistant", "content": response.content})
    with st.chat_message("assistant"):
        st.write(response.content)