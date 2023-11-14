import streamlit as st
import cohere
import random

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

oPages = [  
        {  
            "id": "web-search_1",  
            "title": "Miami Real Estate",  
            "snippet": "Miami-Dade county has some of the most beautiful neighborhoods in South Florida. Golfing, sailing, boating, beach life, night life, luxury shopping and dining, natural parks, are just a few of the amenities found in Miami's amazing communities!",  
            "url": "https://www.miamirealestate.com"  
        },  
        {  
            "id": "web-search_2",  
            "title": "Maiami Real Estate - Luxury Listings",  
            "snippet": "Let Us Help You Find Your Place In The World.",  
            "url": "https://www.miamirealestate.com/miami-luxury-listings/"  
        },  
        {  
            "id": "web-search_3",  
            "title": "Maiami Real Estate - A Day In Miami",  
            "snippet": "Take pleasure in an early morning walk along miles of white sand beaches and delight in the melodic lapping waves of the blue Atlantic Ocean along the shoreline.",  
            "url": "https://www.miamirealestate.com/miami-living/"  
        },  
        {  
            "id": "web-search_4",  
            "title": "Maiami Real Estate - For Buyers",  
            "snippet": "Many exclusive homes never make it to the MLS service, because the agents who represent the sellers introduce the property selectively. Agents who are familiar with the luxury market know that finding a buyer is often a matter of great detective work. For every upscale home, there is an ideal buyer among a target group with a high probability of interest in such a property.",  
            "url": "https://www.miamirealestate.com/for-buyers/"  
        },  
        {  
            "id": "web-search_5",  
            "title": "Maiami Real Estate - Our Company",  
            "snippet": "Our goal is to provide the ultimate in professional residential and commercial real estate service to the most affluent customers, focusing on properties in the upper level marketplace which serve the needs of a sophisticated clientele.",  
            "url": "https://www.miamirealestate.com/our-company/"  
        }  
    ]


def  generate_article(prompt : str):
    response = co.chat(
        stream=False,
        max_tokens=800,
        message=prompt,
        model="command-nightly", 
        temperature=0.5,
        prompt_truncation='auto',
        documents=oPages,      
    )

    generated_content = response.text
    return  generated_content



def  generate_answer(prompt : str, oHistory: list = []):
    response = co.chat(
        chat_history=st.session_state.messages,
        stream=False,
        max_tokens=800,
        message=prompt,
        model="command-nightly", 
        temperature=0.5,
        prompt_truncation='auto',
        documents=oPages,      
    )

    generated_content = response.text
    return  generated_content

def clear_input():
    st.session_state.enter_topic = ""

def initialize_session_state():
    st.session_state.messages = []
    st.session_state.topic = ""
    st.session_state.article_name = ""   # request to generate
    st.session_state.article_text = ""   # generated text

cohere_api_key = st.secrets["cohere_api_key"];
co = cohere.Client(cohere_api_key)

# Accessing the query parameters
# Query parameters are returned as a dictionary
query_params = st.experimental_get_query_params()

# [""] is a fallback value if the parameter isn't found
param_values = query_params.get('q', [""]) 
q = param_values [0]

# initialize variable in session state
if "messages" not in st.session_state:
    initialize_session_state();

if "topic" not in st.session_state:
    st.session_state.topic = ""
if "article_name" not in st.session_state:
    st.session_state.article_name = ""
if "article_text" not in st.session_state:
    st.session_state.article_text = ""

if q:
    st.session_state.topic = q
    st.session_state.article_name = q

generated_content = ""

if st.session_state.topic == "":
    # Create a text input widget in the sidebar
    topic_value = st.sidebar.text_input("Enter a topic", value=st.session_state.topic, key="enter_topic")

    # Button to manually clear the text input
    if topic_value:
        st.session_state.topic = topic_value
        st.session_state.article_name = topic_value
        st.session_state.article_text == ""
        st.session_state.messages == []

st.sidebar.title(st.session_state.topic)

# Button to manually clear the text input
if st.sidebar.button("New Chat"):
    initialize_session_state();

url = "https://sasson-dialogexpress-app-jkbb2w.streamlit.app/"

if st.session_state.article_text == "":
    if not st.session_state.article_name == "":
        prompt = """.
        Your response should be concise and serious.         
        Write a plain-text encyclopedia article about the following topic: """ + st.session_state.article_name
        generated_content = generate_article(prompt=prompt)
        st.session_state.article_text = generated_content
        st.session_state.messages = []
        # start chat history with the article text
        st.session_state.messages.append({"role":"CHATBOT","message":st.session_state.article_text})
        st.session_state.article_name = ""

# iterate through the messages in the Session State
# and display them in the chat message container
# message["role"] is used because we need to identify user and bot

if len(st.session_state.messages) == 0:
    st.write("Hi!", unsafe_allow_html=True);

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
    
    response = generate_answer(prompt = message_text, oHistory = st.session_state.messages)

    answer = response

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

