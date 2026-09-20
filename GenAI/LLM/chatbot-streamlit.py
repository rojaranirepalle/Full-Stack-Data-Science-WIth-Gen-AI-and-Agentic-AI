from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_TRACING_V2"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "I am a chatbot. I am here to help you with your questions."),
    ("user", "Question:{question}")
])

#streamlit app
st.title("Chatbot Application")
question = st.text_input("Enter your question:")

llm = init_chat_model(
    model="google_genai:gemini-3.6-flash",
    temperature=0.7
)
#llm = ChatOpenAI(model_name="gpt-5.6-luna", temperature=1)
output_parser=StrOutputParser()
chain = prompt_template | llm | output_parser

if question:
    response = chain.invoke({"question": question})
    st.write("Answer:", response)