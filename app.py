import streamlit as st
import cohere
import random


def render_user_message(message):
    st.markdown(
        f"<div style='text-align: right;'><span style='margin-left:200px; color: white; background-color: blue; padding: 10px; border-radius: 5px;'>{message}</span></div><br>",
        unsafe_allow_html=True
    )

def render_chatbot_message(message):
    st.markdown(
        f"<div style='text-align: left; margin-right:50px; color: #111111; padding: 10px; border-radius: 5px;'>{message}</div><br>",        unsafe_allow_html=True
    )

def register_concepts(citations : list):
    oConcepts = []
    
    if citations:
        for oConcept in citations:
            a = oConcept["text"]
            if len(a) >= 6 and len(a) <= 16:
                oConcepts.append(a)

    st.session_state.concepts = oConcepts

def  generate_article(prompt : str):
    """
    if st.session_state.ch == "":
        response = co.chat(
            stream=False,
            max_tokens=800,
            message=prompt,
            model="command-nightly", 
            temperature=2.5,
            prompt_truncation='auto',
            connectors=[{"id": "web-search"}],      
        )
    else:
        response = co.chat  (
            stream=False,
            max_tokens=800,
            message=prompt,
            model="command-nightly", 
            temperature=2.5,
            prompt_truncation='auto',
            connectors= [
                            { "id": "web-search", "options": { "site": st.session_state.ch } } 
                        ]      
        )

    register_concepts(response.citations)
    generated_content = response.text
    """

    return  ""    # generated_content

def  generate_answer(prompt : str, oHistory: list = []):
    """
    response = co.chat(
        chat_history=st.session_state.messages,
        stream=False,
        max_tokens=800,
        message=prompt,
        model="command-nightly", 
        temperature=2.5,
        prompt_truncation='auto',
        connectors=[{"id": "web-search"}],      
    )

    register_concepts(response.citations)
    """
    generated_content = ""  # response.text

    return  generated_content

def clear_input():
    st.session_state.enter_topic = ""

def initialize_session_state(ch : str, q : str):
    st.session_state.ch = ch
    st.session_state.topic = q
    st.session_state.article_name = q    # request to generate an article
    st.session_state.article_text = ""   # generated text
    st.session_state.concepts = []
    st.session_state.messages = []

cohere_api_key = st.secrets["cohere_api_key"];
co = cohere.Client(cohere_api_key)

# Accessing the query parameters
# Query parameters are returned as a dictionary
query_params = st.experimental_get_query_params()

# [""] is a fallback value if the parameter isn't found
param_values1 = query_params.get('q', [""]) 
q = param_values1 [0]
param_values2 = query_params.get('ch', [""]) 
ch = param_values2 [0]

# initialize variable in session state
if "messages" not in st.session_state and "concepts" not in st.session_state :
    initialize_session_state(ch = ch, q = q)

st.session_state.ch = ch
st.session_state.topic = q
st.session_state.article_name = q
generated_content = ""

if isinstance(st.session_state.topic, str):
    st.sidebar.title(st.session_state.topic)

if st.session_state.topic == "":
    if q:
        st.session_state.topic = q
        st.session_state.article_name = q
        st.session_state.article_text == ""
        st.session_state.messages == []

url = "https://sasson-dialogexpress-app-jkbb2w.streamlit.app/"

if st.session_state.article_text == "":
    if not st.session_state.article_name == "":
        prompt = """.
        Your response should be concise and serious.         
        Write a plain-text encyclopedia article about the following subject: """ + st.session_state.article_name
        generated_content = generate_article(prompt=prompt)
        st.session_state.article_text = generated_content
        st.session_state.messages = []
        # start chat history with the article text
        st.session_state.messages.append({"role":"CHATBOT","message":st.session_state.article_text})
        st.session_state.article_name = ""


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
        st.write(f"UNEXPECTED ROLE {role}", unsafe_allow_html=True)

hint_text = "Say something"

# check if user made a chat input 
input_text = st.chat_input(hint_text, key="chat_input")
if input_text:
    # Display the most recent user message
    render_user_message(message = input_text)
    st.write(f"<br>", unsafe_allow_html=True)

    # and add it to the list of messages
    st.session_state.messages.append({"role": "USER", "message": input_text})

    message_text = """Act as an AI expert. 
        Continue a nice, informal conversation. 
        Your response should be both concise and serious:         
        """ +  input_text
    
    # response = generate_answer(prompt = message_text, oHistory = st.session_state.messages)

    answer = ""   # response

    render_chatbot_message(message = answer)
    st.write(f"<br>", unsafe_allow_html=True)

    # add the echo message to chat history
    st.session_state.messages.append( {"role":"CHATBOT","message":answer} )

    L = len(st.session_state.messages) 
    
    if L == 0:
        if not st.session_state.article_text == "":
            # insert article_text
            st.session_state.messages.append({"role":"CHATBOT","message":st.session_state.article_text})

    LIMIT = 10
    if L > LIMIT:
        # reduced list of messages alwais starts with an article text, if present
        st.session_state.messages = [st.session_state.article_text] + st.session_state.messages [ - LIMIT:]

