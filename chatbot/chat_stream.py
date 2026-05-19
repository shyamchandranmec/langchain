from langchain_core.prompts import (MessagesPlaceholder)
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate)
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
load_dotenv()

import streamlit as st
load_dotenv()
user_id = st.text_input("Enter your user ID", key="user_id", value="default_user")

def get_session_history(session_id: str):
    return SQLChatMessageHistory(session_id=session_id, connection="sqlite:///chat_history.db")


st.title("Make your own chatbot")
if (st.button("Start a new chat session")):
    st.session_state["chat_history"] = []
    history = get_session_history(user_id)
    history.clear()

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for message in st.session_state["chat_history"]:
    with st.chat_message(message.type):
        st.write(message.content)


llm = ChatOpenAI(model="gpt-5.4-mini")
system_message = SystemMessagePromptTemplate.from_template(
    "You are a helpful assistant.")
human_message = HumanMessagePromptTemplate.from_template("{input}")
prompt = ChatPromptTemplate.from_messages([system_message, human_message])
chain = prompt | llm | StrOutputParser()
runnable_with_history = RunnableWithMessageHistory(chain, get_session_history)


def chat_with_llm(session_id: str, user_input: str):
    return runnable_with_history.invoke(
        {"input":user_input},
        config={"configurable": {"session_id": session_id}}
    )

prompt = st.chat_input("You: ", key="input")

if prompt:
    st.session_state["chat_history"].append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.write(prompt)
    response = chat_with_llm(user_id, prompt)
    with st.chat_message("assistant"):
        st.write(response)
    st.session_state["chat_history"].append(AIMessage(content=response))