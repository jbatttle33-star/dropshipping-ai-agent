import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
import json

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=st.secrets["GROQ_API_KEY"])

st.title("My AI Dropshipping Assistant")

# Persistent memory using Streamlit storage
if "messages" not in st.session_state:
    if "saved_messages" in st.session_state:
        st.session_state.messages = st.session_state.saved_messages
    else:
        st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.saved_messages = st.session_state.messages

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
    st.session_state.saved_messages = st.session_state.messages

    with st.chat_message("assistant"):
        st.write(response.content)

if st.button("Clear Memory"):
    st.session_state.messages = []
    st.session_state.saved_messages = []
    st.rerun()
