import streamlit as st
import cohere

class Agent:
    def __init__(self, ch : str, start : str):
        self.ch = ch
        self.start = start
        self.generated_content = ""

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
                if len(a) >= 10 and len(a) <= 20:
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

        try:
            response = self.co2.chat(
                chat_history=self.messages,
                stream=False,
                max_tokens=800,
                message=message,
                model="command-light", 
                temperature=1.5,
                prompt_truncation='auto',
                connectors=connectors,
            )
        except Exception as ex:
            st.sidebar.write(ex)
        finally:
            pass

        self.generated_content = response.text
        self.register_concepts(response.citations)
        self.register_results(response.documents)

        return  response.text

    def adjust_messages(self, LIMIT : int = 10):
        # reduce the list of messages 
        if len(self.messages) > LIMIT:
            self.messages = self.messages [-LIMIT:]

    def is_valid_string(self, s : str):
        punctuation=",;.:-"

        # Check if each character in the string is alphanumeric, 
        # a whitespace, 
        # or in the punctuation string
        for char in s:
            if not (char.isalnum() or char.isspace() or char in punctuation):
                return False
        return True
