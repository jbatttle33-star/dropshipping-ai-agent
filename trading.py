import streamlit as st
import requests
import json

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

SYSTEM_PROMPT = """You are an expert stock and crypto trading assistant.
Your jobs are:
1. CHART ANALYSIS — Analyze technical indicators and patterns
2. TRADE SIGNALS — Suggest buy, sell or hold signals
3. RISK MANAGEMENT — Calculate position sizes and stop losses
4. MARKET NEWS — Connect news to price movements
5. TRADE JOURNAL — Log and track all trades

Always include entry price, stop loss, take profit and risk level."""

def ask_groq(messages):
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": messages
        }
    )
    return response.json()["choices"][0]["message"]["content"]

st.title("AI Trading Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask about any stock or trade...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(st.session_state.messages)

    response = ask_groq(messages)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.write(response)

if st.button("Clear Memory"):
    st.session_state.messages = []
    st.rerun()