import streamlit as st
import yaml
from datetime import time

class Chat:
    def __init__(self, chat_name:str):
        self.chat_name = chat_name

class Chats:
    def __init__(self):
        self.chats = {}
    
    def add(self, chat : Chat):
        self.chats[chat.chat_name] = chat;
     
    def get_list(self):
        oList = []
        for chat in self.chats.values:
            oList.append(chat);
            
        
        
# Define app
def app():
    chat = Chat("simple")
    
    # Set page title and favicon
    st.set_page_config(page_title="Dialog Express", page_icon=":hibiscus:")

    if not "chats" in st.session_state:
        st.session_state["chats"] = Chats()

    # Add sidebar with options
    #st.sidebar.title("Dialog History")

    answer = st.text_input("Your answer:")
    if answer:
        st.write(answer)

    # Add file uploader for questions and answers
    file = st.file_uploader("Upload questions and answers", type=["yaml"])
    
    questions = []

    # Read questions and answers from file
    if file:
        data = yaml.safe_load(file)
        questions = data

        # Display questions and answers
        for i, qa in enumerate(questions):
            # write the question
            q = qa [0]
            st.write(q)
            
            # write all answers
            for a in qa[1]:
                st.write(a)



    else:
        # Use default questions if no file is uploaded
        questions = []
    
if __name__ == '__main__':
    app()

