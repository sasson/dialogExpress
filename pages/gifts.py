import streamlit as st
from agents import Agent
from dialog_page import DialogPage, remove_query_parameters

page_name = "gifts"
page_channel ="amazon.com"

DialogPage.start(page_name = page_name, page_channel = page_channel)

page = st.session_state.page

page.initialize(page_name = page_name, page_channel = page_channel, prompt = f"""
Help to find and disuss gifts.
Please, keep conversation friendly and 'safe for work'.  
Please write a short informal response based on gifts found. 
Question:                
""" 
)

# display agent's channel in the sidebar
if isinstance(page.agent.ch, str):
    st.sidebar.title(page.page_name)
    st.sidebar.write(page.page_channel)

page.render_messages()

# check if user made a chat input
input_text = st.chat_input("Say something", key="chat_input")
if input_text:    
    page.on_input(input_text = input_text)

remove_query_parameters()
