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

    start_message = """
    I'm excited to show off my world knowledge and have a fun chat with you. 
    Let's make this a breeze!
    """
    render_chatbot_message(message=start_message)

# iterate through the messages in the Session State
# and display them in the chat message container
# message["role"] is used because we need to identify user and bot

for message_object in st.session_state.messages:
    role = message_object["role"]
    message = message_object["message"]

    if role == "USER":
        render_user_message(message = message)
    elif role == "CHATBOT":
        render_chatbot_message(message = message)
    else:
        st.write(f"UNEXPECTED ROLE {role}")

hint_text = "Say something"

# check if user made a chat input 
input_text = st.chat_input(hint_text)
if input_text:
    # Display user message
    render_user_message(message = input_text)
    st.write(f"<br>", unsafe_allow_html=True)

    # add message to history
    st.session_state.messages.append({"role": "USER", "message": input_text})

    message_text = """
        Continue a nice, informal conversation, with short answers. 
        You are an expert of world knowledge. 
        I am going to ask you a question. 
        Your response should be concise but fun and friendly.
        But no 'feel free to ask' type pushing! :        
        """ +  input_text
    response = co.chat(
        chat_history=st.session_state.messages,
        max_tokens=800,
        message=message_text,
        model="command-nightly", 
	    temperature=1.0,
        prompt_truncation='auto',
        connectors=[{"id": "web-search"}]
    )

    answer = response.text

    render_chatbot_message(message = answer)
    st.write(f"<br>", unsafe_allow_html=True)

    # add the echo message to chat history
    st.session_state.messages.append({"role":"CHATBOT","message":answer})

    L = len(st.session_state.messages) 
    if L > 12:
        st.session_state.messages = st.session_state.messages[-12:]
