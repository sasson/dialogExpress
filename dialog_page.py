import streamlit as st

from text import Text
from agents import Agent

class DialogPage():
    @staticmethod
    def start(page_name : str, page_channel : str):
        if not "page" in st.session_state:
            st.session_state.ignore_q = False
            st.session_state.page = DialogPage(page_name = page_name, page_channel = page_channel)

        if st.session_state.page.page_name == page_name:
            st.session_state.ignore_q = False
        else:
            st.session_state.ignore_q = True
            st.session_state.page = DialogPage(page_name = page_name, page_channel = page_channel)

    def __init__(self, page_name: str, page_channel: str = "", prompt: str = ""):
        self.page_name = page_name
        self.page_channel = page_channel
        self.prompt = prompt
        self.agent = None

    def initialize(self, page_name : str, page_channel : str, prompt : str):
        if st.session_state.ignore_q:
            # switching to a new, different page by clicking on the left sidebar
            new_start = ""
        else: 
            # Accessing the query parameters
            # Query parameters are returned as a dictionary
            query_params = st.experimental_get_query_params()
            # [""] is a fallback value if the parameter isn't found
            param_values = query_params.get('q', [""]) 
            new_start = param_values [0]

        self.prompt = prompt

        needs_starting_answer = False
        if self.agent == None:
            self.agent = Agent(ch = page_channel, start=new_start)
            if not new_start == "":
                needs_starting_answer = True

        if not new_start == self.agent.start:
            self.agent.start = new_start
            needs_starting_answer = True

        if needs_starting_answer and not new_start == "" and not st.session_state.ignore_q:
            answer_text = self.agent.generate_answer(prompt = self.prompt, input_text = new_start)

            # add the answer to chat history
            self.agent.messages.append( {"role":"CHATBOT", "message":answer_text} )

    def on_input(self, input_text : str = ""):
        # display the most recent user message
        self.render_user_message(message = input_text)
        # add it to the list of messages
        self.agent.messages.append({"role": "USER", "message": input_text})
        st.write(f"<br>", unsafe_allow_html=True)

        if not input_text == "":
            # get the answer
            answer_text = self.agent.generate_answer(prompt = self.prompt, input_text = input_text)

            # add the answer to chat history
            self.agent.messages.append( {"role":"CHATBOT", "message":answer_text} )
    
            # display the answer
            st.write(f"<br>", unsafe_allow_html=True)
            self.render_chatbot_message(generated_content = answer_text)

            # avoid keeping too many messages in the list
            self.agent.adjust_messages(LIMIT = 20)

    def simplify (self, s : str):
        """
        This function takes a string 's' and returns the same string with all non-alphanumeric
        characters replaced by a space.
        """
        # Using a list comprehension for efficiency
        result = ''.join([char if char.isalnum() else ' ' for char in s])
        result = result.replace("  ", " ").strip()
        if len(result) > 100:
            result = result[:100]

        return  result

    def generate_html_for_result(self, oResult):
        id = self.simplify(oResult["id"]).replace(" ","-")
        snippet = oResult["snippet"]
        title = oResult["title"]
        url = oResult["url"]
        description = self.simplify(snippet)

        return f"""<div id="{id}">
            <a href="{url}" 
               style="color:#blue; font-weight:bold; " 
               target="_blank" 
            >{title}</a>
        </div>
        <div>
            {description}
        </div>
        """

    def generate_html_for_token(self, tag : str, content : str) -> str:
        # Generates HTML based on the tag, content, and url (for links)
        if tag == "text":
            # Return plain text content for text tags
            return " " + content
        elif tag == "link":
            # Generate a span with a style for color-coded content
            # Format the content for the URL query string
            query_content = content.replace("."," ").replace("  "," ").replace(" ", "+")
            return f'<a href="?q={query_content}" style="color:blue;" target="_self">{content}</a>'
        else:
            # Default case returns content as is
            return f'<span style="color:red;">{content}</span>'

    def generate_html_for_answer(self, oText:Text) -> str:
        # Generates HTML for all tokens in the list, using url for links
        formatted_tokens = [self.generate_html_for_token(tag, content) for (tag, content) in oText.tokens]
        s = " ".join(formatted_tokens)
        s = s.replace("\n\n", "<br />")

        return s

    def generate_html_for_results(self) -> str:
        # Generates HTML for all tokens in the list

        urls = []   # to avoid the repetition of links

        result_html = ""
        for result in self.agent.results:
            url : str = result["url"]

            if not url in urls and self.agent.ch in url:
                html : str = self.generate_html_for_result(result)
                result_html += html + "<br>"
                urls.append(url)

        return  result_html

    def render_user_message(self, message):
        html = f"""
        <div style='text-align: right;'>
            <span style='margin-left:200px; color: white; background-color: blue; padding: 10px; border-radius: 5px;'>{message}</span>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    def render_chatbot_message(self, generated_content : str):
        st.markdown(self.generate_html_for_results(), unsafe_allow_html=True)

        oText = Text(generated_content = generated_content, concepts = self.agent.concepts)
        st.markdown(self.generate_html_for_answer(oText=oText), unsafe_allow_html=True)

    def render_message(self, message_object):
        # message["role"] is used because we need to identify user and bot

        role = message_object["role"]
        message = message_object["message"]

        if role == "USER":
            self.render_user_message(message = message)
        elif role == "CHATBOT":
            self.render_chatbot_message(generated_content = message)
        else:
            st.write(f"UNEXPECTED ROLE {role}", unsafe_allow_html=True)

    # iterate through the messages in the Session State
    # and display them in the chat message container
    def render_messages(self):
        st.title(self.agent.start)
        st.write("")
        for message_object in self.agent.messages:
            self.render_message(message_object)

def remove_query_parameters():
    js = """
    <script>
    const url = new URL(window.location);
    url.search = ''; // Remove query parameters
    window.history.replaceState({}, document.title, url);
    </script>
    """
    st.markdown(js, unsafe_allow_html=True)