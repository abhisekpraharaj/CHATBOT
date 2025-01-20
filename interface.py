import streamlit as st
import requests

st.set_page_config(page_title = "LangGraph Agent User Interface", layout = "centered")

API_URL = "http://127.0.0.1:8000/machine"

MODELS = [
    "llama3-70b-8192",  # Model 1
    "mixtral-8x7b-32768",  # Model 2
    "distil-whisper-large-v3-en", # Model 3
    "gemma2-9b-it" #Model 4
]

# Title and Description
st.markdown('<p class="title">LangGraph Agent Chatbot</p>', unsafe_allow_html=True)
st.write("Interact with the AI agent by selecting the model and giving it a title, then ask your queries.")

# Define Your AI Agent Section
st.markdown('<p class="header">Define Your AI Agent</p>', unsafe_allow_html=True)
given_prompt = st.text_area("Type a description for the AI agent (e.g., 'You are a researcher.')", height=100, placeholder="Type your system prompt here...", key="system_prompt")

# Select Model Section
st.markdown('<p class="header">Select AI Model</p>', unsafe_allow_html=True)
selected_model = st.selectbox("Choose a Model", MODELS, key="model_selector", index=0)

# User Input Section
st.markdown('<p class="header">Your Message</p>', unsafe_allow_html=True)
user_input = st.text_area("Enter your message(s)", height=150, placeholder="Type your message here...", key="user_input")

if st.button("Submit"):
    if user_input.strip():
        try:
            payload = {"messages": [user_input], "model": selected_model, "prompt": given_prompt}
            response = requests.post(API_URL, json = payload)
            if response.status_code == 200:
                response_data = response.json()
                if "error" in response_data:
                    st.error(response_data["error"])
                else:
                    ai_responses = [
                        message.get("content", "")
                        for message in response_data.get("messages", [])
                        if message.get("type") == "ai"
                    ]

                    if ai_responses:
                        st.subheader("Agent Response:")
                        st.markdown(f"**Final Response:** {ai_responses[-1]}")
                        # for i, response_text in enumerate(ai_responses, 1):
                        #     st.markdown(f"**Response {i}:** {response_text}")
                    else:
                        st.warning("No AI response found in the agent output.")
            else:
                st.error(f"Request failed with status code {response.status_code}.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a message before clicking 'Send Query'.")