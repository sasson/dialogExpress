import streamlit as st
import cohere
import random
from agents import Agent

def initialize_session_state(ch : str, q : str):
    st.session_state.agent = Agent(ch = ch, q = q)

page_channel = "inner.org"

# Accessing the query parameters
# Query parameters are returned as a dictionary
query_params = st.experimental_get_query_params()

# [""] is a fallback value if the parameter isn't found
param_values = query_params.get('q', [""]) 
q = param_values [0]

# initialize variable in session state
if "agent" not in st.session_state or st.session_state.agent.ch != page_channel:
    initialize_session_state(ch = page_channel, q = q)

    # curl = "https://sasson-dialogexpress-app-jkbb2w.streamlit.app/"

agent = st.session_state.agent
if isinstance(agent.ch, str):
    st.sidebar.title(agent.ch)

# iterate through the messages in the Session State
# and display them in the chat message container
# message["role"] is used because we need to identify user and bot
st.session_state.agent.render_messages()

# check if user made a chat input 
hint_text = "Say something"
input_text = st.chat_input(hint_text, key="chat_input")
if input_text:
    agent = st.session_state.agent 

    # Display the most recent user message
    # and add it to the list of messages
    agent.render_user_message(message = input_text)
    agent.messages.append({"role": "USER", "message": input_text})

    st.write(f"<br>", unsafe_allow_html=True)

    prompt = f"""You are an Innovative Dialog Search Engine for Kabbalah & Chassidism.
Please, keep conversation friendly and concise and 'safe for work'.  
Based only on {agent.ch}, please write a short encyclopedia article 
describing what is found with respect to: 
""" 
    answer_text = agent.generate_answer(prompt = prompt, input_text = input_text)

    # add the answer to chat history
    agent.messages.append( {"role":"CHATBOT", "message":answer_text} )

    st.write(f"<br>", unsafe_allow_html=True)
    agent.render_chatbot_message()


    # reduce the list of messages 
    LIMIT = 10
    if len(st.session_state.agent.messages) > LIMIT:
        st.session_state.agent.messages = st.session_state.agent.messages [-LIMIT:]
