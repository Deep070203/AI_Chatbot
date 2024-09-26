# Import necessary modules
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain.schema import(SystemMessage, HumanMessage, AIMessage)
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
clear_button = st.sidebar.button("Clear Conversation", key="clear")
if clear_button or "messages" not in st.session_state:
    st.session_state.messages = [
      SystemMessage(
        content="you are a helpful AI assistant. Reply your answer in markdown format."
      )
    ]

# Create a chain that combines the prompt and the Ollama model
chain=prompt|llm

# Invoke the chain with the input text and display the output
if input_text:
    st.session_state.messages.append(HumanMessage(content=input_text))
    with st.spinner("Bot is typing ..."):
      answer = chain.invoke({"question":input_text})
      print(answer)
    st.session_state.messages.append(AIMessage(content=answer))
    # st.write(chain.invoke({"question":input_text}))

messages = st.session_state.get("messages", [])
for message in messages:
    if isinstance(message, AIMessage):
      with st.chat_message("assistant"):
        st.markdown(message.content)
    elif isinstance(message, HumanMessage):
      with st.chat_message("user"):
        st.markdown(message.content)
