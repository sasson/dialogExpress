import sys
import streamlit as st
import toml
from dialog_page import DialogPage
from channel_definition import ChannelDefinition

no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

definition = ChannelDefinition(
    name = "youtube", 
    domain = "youtube.com", 
    prompt = """
Discuss and help to find interresting stuff.
Please, keep conversation 'safe for work', friendly and concise.
Please discuss news and politics. 
Answer the question:   
"""
)

query_params = st.experimental_get_query_params()
# [""] is a fallback value if the parameter isn't found
q = query_params.get('q', [""]) [0]

# Create an instance of DialogPage
page = DialogPage(definition = definition, q = q)
st.session_state.page = page

# Display channel name and domain in the sidebar
if isinstance(page.name, str):
    st.sidebar.title(page.name)

page.render_messages()

# check if user made a chat input
input_text = st.chat_input("Say something", key="chat_input")
if input_text:    
    page.on_input(input_text = input_text)
