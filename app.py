import streamlit as st
import cohere

cohere_api_key = st.secrets["cohere_api_key"];
co = cohere.Client(cohere_api_key)

st.sidebar.title("Dialog Express")

def render_user_message(message):
    st.markdown(
        f"<div style='text-align: right;'><span style='margin-left:200px; color: white; background-color: blue; padding: 10px; border-radius: 5px;'>{message}</span></div><br>",
        unsafe_allow_html=True
    )

def render_chatbot_message(message):
    st.markdown(
        f"<div style='text-align: left; margin-right:50px; color: #111111; padding: 10px; border-radius: 5px;'>{message}</div><br>",        unsafe_allow_html=True
    )

# initialize the Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# iterate through the messages in the Session State
# and display them in the chat message container
# message["role"] is used because we need to identify user and bot

chat_history = []
context = ""
for message_object in st.session_state.messages:
    role = message_object["role"]
    message = message_object["message"]

    if role == "USER":
        render_user_message(message = message)
    elif role == "CHATBOT":
        render_chatbot_message(message = message)
    else:
        st.write(f"UNEXPECTED ROLE {role}")

soft_text = "Say something"
# check if user made a chat input 
prompt = st.chat_input(soft_text)
if prompt:
    # Display user message
    render_user_message(message = prompt)
    st.write(f"<br>", unsafe_allow_html=True)

    # add message to history
    st.session_state.messages.append({"role": "USER", "message": prompt})

    response = co.chat(
        chat_history=st.session_state.messages,
        message= "Continue a nice, friendly conversation, wuth five to ten line entertaining answers. " +  prompt,
        model="command-nightly", 
	    temperature = 2.0,
        prompt_truncation='auto',
        connectors=[{"id": "web-search"}]
    )

    answer = response.text

    render_chatbot_message(message = answer)
    st.write(f"<br>", unsafe_allow_html=True)

    # add the echo message to chat history
    st.session_state.messages.append({"role":"CHATBOT","message":answer})

    if len(st.session_state.messages) > 30:
        st.session_state.messages = st.session_state.messages[-30:]