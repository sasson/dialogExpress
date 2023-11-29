import streamlit as st
import cohere
from text import Text

class Agent:
    def __init__(self, ch : str = "" , q : str = "" ):
        self.ch = ch
        self.topic = q
        self.generated_content = ""

        self.base_url = "https://sasson-dialogexpress-app-jkbb2w.streamlit.app"

        self.concepts = []
        self.results = []
        self.messages = []

        cohere_api_key = st.secrets["cohere_api_key"];
        self.co1 = cohere.Client(cohere_api_key)

        cohere_api_key_pro = st.secrets["cohere_api_key_pro"];
        self.co2 = cohere.Client(cohere_api_key_pro)

    def register_concepts(self, citations : list):
        oConcepts = []
        
        if citations:
            for oConcept in citations:
                a = oConcept["text"]
                if len(a) >= 6 and len(a) <= 36:
                    oConcepts.append(a)

        self.concepts = oConcepts

    def register_results(self, documents : list):
        oDocuments = []
        
        if documents:
            for oDocument in documents:
                 oDocuments.append(oDocument)

        self.results = oDocuments


    def  generate_answer(self, prompt : str, input_text : str):
        if self.ch == "":
            connectors = [ {"id": "web-search"} ]
        else:
            connectors = [ {"id": "web-search","options": {"site": self.ch}} ]

        message = prompt + " " + input_text

        response = self.co2.chat(
            chat_history=self.messages,
            stream=False,
            max_tokens=800,
            message=message,
            model="command-nightly", 
            temperature=1.5,
            prompt_truncation='auto',
            connectors=connectors,
        )

        self.generated_content = response.text
        self.register_concepts(response.citations)
        self.register_results(response.documents)

        return  response.text

    def generate_html_for_token(self, tag : str, content : str) -> str:
        # Generates HTML based on the tag, content, and url (for links)
        if tag == "text" or tag == "link":
            # Return plain text content for text tags
            return f'<span style="color:#484848;">{content}</span>'
        elif tag == "":
            # Generate a span with a style for color-coded content
            # Format the content for the URL query string
            query_content = content.replace("."," ").replace("  "," ").replace(" ", "+")
            return f'<a href="?q={query_content}" style="color:#489add;" target="_self">{content}</a>'
        else:
            # Default case returns content as is
            return f'<span style="color:#DD4848;">{content}</span>'
        
    def generate_html_for_result(self, oResult):
        id = oResult["id"]
        # snippet = oResult["snippet"]
        title = oResult["title"]
        url = oResult["url"]

        return f"""<div>
        <a href="{url}" style="color:#489add; font-weight:700; " 
        target="_blank" >{title}</a>
        </div>"""

    def generate_html_for_answer(self, oText:Text) -> str:
        # Generates HTML for all tokens in the list, using url for links
        formatted_tokens = [self.generate_html_for_token(tag, content) for (tag, content) in oText.tokens]
        return " ".join(formatted_tokens) + "\n<br>"

    def generate_html_for_results(self) -> str:
        # Generates HTML for all tokens in the list

        urls = []   # to avoid the repetition of links

        result_html = ""
        for result in self.results:
            url = result["url"]
            if not url in urls and self.ch in url:
                html = self.generate_html_for_result(result)
                result_html += "<br>" + html + "<br>"
                urls.append(url)
        result_html += "<br>"

        return  result_html

    def render_user_message(self, message):
        html = f"""
        <div style='text-align: right;'>
            <span style='margin-left:200px; color: white; background-color: blue; padding: 10px; border-radius: 5px;'>{message}</span>
        </div>
        <br>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    def render_chatbot_message(self):
        oText = Text(generated_content = self.generated_content, concepts = self.concepts)
        st.markdown(self.generate_html_for_results(), unsafe_allow_html=True)
        st.markdown(self.generate_html_for_answer(oText=oText), unsafe_allow_html=True)

    def render_messages(self):
        for message_object in self.messages:
            role = message_object["role"]
            message = message_object["message"]

            if role == "USER":
                self.render_user_message(message = message)
            elif role == "CHATBOT":
                self.render_chatbot_message()
            else:
                st.write(f"UNEXPECTED ROLE {role}", unsafe_allow_html=True)
        