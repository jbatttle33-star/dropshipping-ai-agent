import streamlit as st
import requests
import json

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

SYSTEM_PROMPT = SYSTEM_PROMPT = """You are an expert trading assistant connected to TradingView.

Your specific jobs are:
1. STOCK ANALYSIS — Analyze any stock ticker like AAPL, TSLA, NVDA
2. CRYPTO ANALYSIS — Analyze BTC, ETH, SOL and other crypto
3. TECHNICAL ANALYSIS — Read RSI, MACD, Moving Averages
4. TRADE SIGNALS — Give clear BUY, SELL or HOLD signals
5. RISK MANAGEMENT — Always give stop loss and take profit levels
6. MARKET NEWS — Connect current news to price movements
7. TRADING JOURNAL — Help track and log all trades

For every analysis always provide:
- Current trend direction
- Key support and resistance levels
- RSI reading and what it means
- MACD signal
- Recommended entry price
- Stop loss level
- Take profit target
- Risk to reward ratio
- Confidence level out of 10
- Final recommendation: BUY, SELL or HOLD

Always be specific with numbers and prices.
Never give vague advice — always be clear and actionable."""

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
