## Conversational ChatBot
import streamlit as st

from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_community.chat_models import ChatOpenAI

st.set_page_config(page_title="UOB Multilingual Chatbot")
st.header("What You Want?")

from dotenv import load_dotenv
load_dotenv()

import os
api_key = os.getenv("API_KEY")

chat = ChatOpenAI(api_key=api_key,temperature=0)

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


input = st.text_input("Anything also can?", key = "input")
response = get_chat_model_response(input)
submit = st.button("Ask the question")


if submit:
    st.subheader("The answer to your stupid question is")
    st.write(response)
