import streamlit as st
from groq import Groq

# Load FAQ knowledge base
try:
    with open(r'C:\Users\Visweswaran\Pictures\python\knowledge_base.txt', 'r', encoding="utf-8") as file:
        content = file.read()
except FileNotFoundError:
    st.error("⚠️ The knowledge base file does not exist. Please check the path.")
    content = ""

# Initialize Groq client
client = Groq(api_key="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")   # 🔑 replace with your API key

# System message
system_prompt = {
    "role": "system",
    "content": f"""
You are a friendly customer support chatbot for 'Chai & Coffee Express'.
You must use the following knowledge base to answer customer queries:

{content}

If the knowledge base does not contain the answer, politely say:
"Sorry, I don’t have that information. Please contact our staff for details."
"""
}

# Streamlit UI
st.set_page_config(page_title="AI Customer Support Chatbot", page_icon="☕", layout="centered")

st.title("🤖 Chai & Coffee Express - AI Customer Support Demo")
st.caption("Ask me anything about our café — opening hours, menu, delivery, payments, and more!")

# Session state to store chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! 👋 I’m your café assistant. How can I help you today?"}]

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# Chat input box
if prompt := st.chat_input("Type your question..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Prepare messages
    messages = [system_prompt] + st.session_state.messages

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",  # good balance
            messages=messages
        )
        reply = response.choices[0].message.content

    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    # Add assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)
