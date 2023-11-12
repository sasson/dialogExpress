import streamlit as st
import cohere
import random

url = "https://sasson-dialogexpress-app-jkbb2w.streamlit.app/"

oList = [
"Albania",
"Tirana",
"Armenia",	
"Yerevan",
"Australia", 	
"Canberra",
"Austria",	
"Vienna",
"Azerbaijan", 	
"Baku",
"Belarus",     
"Minsk",
"Belgium", 	
"Brussels",
"Bulgaria",	
"Sofia",
"Canada",	
"Ottawa",
"Croatia",
"Zagreb",
"Cyprus",
"Nicosia",
"Denmark",	
"Copenhagen",
"England", 	
"London",
"Estonia",	
"Tallinn",
"Finland",	
"Helsinki",
"France",
"Paris",
"Georgia", 	
"Tbilisi",
"Germany", 	
"Berlin",
"Greece",
"Athens",
"Hungary",	
"Budapest",
"Iceland",	
"Reykjavik",
"Ireland",
"Dublin",
"Israel",
"Jerusalem",
"Italy",
"Rome",
"Latvia",
"Riga",
"Luxembourg",
"Monaco",
"Netherlands", 	
"Amsterdam",
"Norway",
"Oslo",
"Poland", 	
"Warsaw",
"Portugal", 	
"Lisbon",
"Romania",	
"Bucharest",
"Russia",
"Moscow",
"Scotland", 	
"Edinburgh",
"Serbia",
"Belgrade",
"Slovakia",	
"Bratislava",
"Slovenia",
"Ljubljana",
"Spain",
"Madrid",
"Sweden",
"Stockholm",
"Switzerland", 	
"Bern",
"Turkey", 	
"Ankara",
"Ukraine",	
"Kiev",
"Vatican City",
"Wales",
"Cardiff" ]

def render_user_message(message):
    st.markdown(
        f"<div style='text-align: right;'><span style='margin-left:200px; color: white; background-color: blue; padding: 10px; border-radius: 5px;'>{message}</span></div><br>",
        unsafe_allow_html=True
    )

def render_chatbot_message(message):
    st.markdown(
        f"<div style='text-align: left; margin-right:50px; color: #111111; padding: 10px; border-radius: 5px;'>{message}</div><br>",        unsafe_allow_html=True
    )

def  generate_content(topic):
    prompt = """
        You are an expert of world knowledge. 
        Write a short plain text article about this topic: 
        """ +  topic
    response = co.generate(
        prompt=prompt,
        model="command-nightly"
    )

    generated_content = response.generations[0].text
    
    return  generated_content


cohere_api_key = st.secrets["cohere_api_key"];
co = cohere.Client(cohere_api_key)

# Accessing the query parameters
query_params = st.experimental_get_query_params()
# Query parameters are returned as a dictionary

# You can access specific parameters like this:
#  param_value = query_params.get('q', ['default_value'])[0]
# 'param_name' is the name of your query parameter
# 'default_value' is a fallback value if the parameter isn't found

# initialize the Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "article" not in st.session_state:
    st.session_state.article = ""
if "article_to_display" not in st.session_state:
    st.session_state.article_to_display = ""

with st.sidebar:
    # Title 
    st.title("Fun-cyclopedia")

generated_content = ""

with st.sidebar:
    # Get Topic
    topic = st.text_input("Enter a topic:", "")
    if topic:
        st.session_state.article = topic
        st.session_state.article_to_display = topic

if st.session_state.article_to_display:
    generated_content = generate_content(st.session_state.article_to_display)
    st.session_state.article_to_display = ""
    with st.sidebar:
        st.markdown(generated_content)

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
