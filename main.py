import openai
import os
import streamlit as st
from dotenv import load_dotenv
import shelve


load_dotenv()

st.title("Welcome to my Ai Chatbot implementation!")

openai.api_key =  os.environ["API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-1106"


def load_chat_history():
    with shelve.open("chat_history.txt") as file:
        return file.get("messages", [])


def save_chat_history(messages):
    with shelve.open("chat_history.txt") as file:
        file["messages"] = messages


if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model = st.session_state["openai_model"],
            messages = [
                {"role": m["role"], "content":m["content"]}
                for m in st.session_state.messages
            ],
            stream = True,
        ):
            full_response += response.choices[0].delta.get("content","")
            message_placeholder.markdown(full_response + " ")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role":"assistant", "content": full_response})        
        
            

with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])




save_chat_history(st.session_state.messages)