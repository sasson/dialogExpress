import streamlit as st
from dialog_page import DialogPage

page_name = "app"
page_channel = ""

base_url = "https://sasson-dialogexpress-app-jkbb2w.streamlit.app"
DialogPage.start(page_name = page_name, page_channel = page_channel)

page = st.session_state.page

# display channel name and domain in the sidebar
if isinstance(page_name, str):
    st.sidebar.title(page.page_name)

page.initialize(page_name = page_name, page_channel = page_channel, prompt = f"""
Please, keep conversation friendly and concise and 'safe for work'.
Please answer describing the found info items that were found. 
Discuss websites selling relevant products and recommended by other websites
The question:   
""" 
)

page.render_messages()

# check if user made a chat input
input_text = st.chat_input("Say something", key="chat_input")
if input_text:    
    page.on_input(input_text = input_text)


