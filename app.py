## Conversational ChatBot
import streamlit as st

from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models.openai import ChatOpenAI

st.set_page_config(page_title="UOB Multilingual Chatbot")
st.header("Ask Me Anything")

from dotenv import load_dotenv
load_dotenv()

import os

chat = ChatOpenAI(temperature=0.5)

if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages']= [
        SystemMessage(content="You are UOB newest Multilingual AI Assistant")
    ]
## Function to load OpenAI Model and get responses
def get_chat_model_response(question):
    st.session_state['flowmessages'].append(HumanMessage(content=question))
    answer = chat(st.session_state['flowmessages'])
    st.session_state['flowmessages'].append(AIMessage(content=answer.content))

    return answer.content


input = st.text_input("What is your question?", key = "input")
response = get_chat_model_response(input)
submit = st.button("Ask the question")


if submit:
    st.subheader("The Response is")
    st.write(response)
