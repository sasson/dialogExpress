import streamlit as st
import cohere
import random

url = "https://sasson-dialogexpress-app-jkbb2w.streamlit.app/"

def get_topics():
    oList = [
"Albania",
"Armenia",	
"Austria",	
"Azerbaijan", 	
"Belarus",     
"Belgium", 	
"Bulgaria",	
"Croatia",
"Cyprus",
"Denmark",	
"England", 	
"Estonia",	
"Finland",	
"France",
"Georgia", 	
"Germany", 	
"Greece",
"Hungary",	
"Ireland",
"Iceland",	
"Israel",
"Italy",
"Latvia",
"Luxembourg",
"Monaco",
"Netherlands", 	
"Norway",
"Poland", 	
"Portugal", 	
"Romania",	
"Russia",
"Scotland", 	
"Serbia",
"Slovakia",	
"Slovenia",
"Spain",
"Sweden",
"Switzerland", 	
"Turkey", 	
"Ukraine",	
"Vatican City",
"Wales",

"Amsterdam",
"Ankara",
"Athens",
"Baku",
"Belgrade",
"Berlin",
"Bern",
"Bratislava",
"Brussels",
"Bucharest",
"Budapest",
"Cardiff",
"Copenhagen",
"Dublin",
"Edinburgh",
"Helsinki",
"Jerusalem",
"Kiev",
"London",
"Lisbon",
"Ljubljana",
"Madrid",
"Minsk",
"Moscow",
"Nicosia",
"Oslo",
"Ottawa",
"Paris",
"Reykjavik",
"Riga",
"Rome",
"Sofia",
"Stockholm",
"Tallinn",
"Tbilisi",
"Tirana",
"Vienna",
"Warsaw",
"Yerevan",
"Zagreb",

 ]

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
        Write a short plain text article 
        about this topic: 
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
# Query parameters are returned as a dictionary
query_params = st.experimental_get_query_params()

# [""] is a fallback value if the parameter isn't found
param_values = query_params.get('q', [""]) 
q = param_values [0]

# initialize the Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "article_name" not in st.session_state:
    st.session_state.article_name = ""
if "article_text" not in st.session_state:
    st.session_state.article_text = ""

with st.sidebar:
    # Title 
    st.title("Fun-cyclopedia")

generated_content = ""

with st.sidebar:
    # Get Topic
    if not q == "":
        topic = q
    else:
        topic = st.text_input("Enter a topic:", "")

    if topic:
        st.session_state.topic = topic
        if st.session_state.article_text == "":
            st.session_state.article_name = topic
    else:
        st.session_state.article_name = ""

if st.session_state.article_text == "":
    if not st.session_state.article_name == "":
        generated_content = generate_content(st.session_state.article_name)
        st.session_state.article_text = generated_content
        st.session_state.messages = []
        # start chat history with the article text
        st.session_state.article_name = ""
        st.session_state.messages.append({"role":"CHATBOT","message":st.session_state.article_text})

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
    # Display the most recent user message
    render_user_message(message = input_text)
    st.write(f"<br>", unsafe_allow_html=True)

    # and add it to the list of messages
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
    
    if L == 0:
        if not st.session_state.article_text == "":
            # insert article_text
            st.session_state.messages.append({"role":"CHATBOT","message":st.session_state.article_text})

    LIMIT = 10
    if L > LIMIT:
        # reduced list of messages alwais starts with an article text, if present
        st.session_state.messages = [st.session_state.article_text] + st.session_state.messages [ - LIMIT:]

