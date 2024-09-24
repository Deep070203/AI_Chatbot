# Import necessary modules
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import streamlit as st

# Set up the Streamlit framework
st.title('Personal Chatbot')  # Set the title of the Streamlit app
input_text=st.text_input("Ask your question!")  # Create a text input field in the Streamlit app

fp = st.sidebar.file_uploader("Upload a PDF file") 

add_selectbox = st.sidebar.selectbox(
    "Choose the LLM",
    ("Llama3.1", "Qwen2.5")
)
# llm_text = st.text_input(add_selectbox)
# Initialize the Ollama model

if add_selectbox == "Llama3.1":
    llm=Ollama(model="llama3.1")
else:
    llm=Ollama(model="qwen2.5:7b")


# Define a prompt template for the chatbot
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please respond to the questions"),
        ("user","Question:{question}")
    ]
)

# Create a chain that combines the prompt and the Ollama model
chain=prompt|llm

# Invoke the chain with the input text and display the output
if input_text:
    st.write(chain.invoke({"question":input_text}))