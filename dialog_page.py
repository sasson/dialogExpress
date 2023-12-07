import streamlit as st
import typing
from typing import Optional, Dict

from text import Text
from channel_definition import ChannelDefinition
from agents import Agent

class DialogPage():
    def __init__(self, definition : ChannelDefinition, q : str):
        self.name = definition.name
        self.domain = definition.domain
        self.prompt = definition.prompt
        self.q = q

        self.agent = Agent(ch = self.name, domain = self.domain, start=self.q)
        if self.q != "":
            answer_text = self.agent.generate_answer(prompt = self.prompt, input_text = self.q)
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
        if len(result) > 400:
            result = result[:400]

            # Splitting the string into words
            words = result.split()
           
            if words:  # Make sure the list is not empty to avoid IndexError
                # Removing the last word
                words = words[:-1]

            # Joining the words back into a string
            result = ' '.join(words) + "..."

        return  result

    def generate_html_for_result(self, oResult):
        id = self.simplify(oResult["id"]).replace(" ","-")
        snippet = oResult["snippet"]
        title = oResult["title"]
        url = oResult["url"]
        description = self.simplify(snippet)

        s = f"""<div class="link" id="{id}">
            <a href="{url}" 
               style="color:#489add; font-weight:bold; " 
               target="_blank" 
            >{title}</a>
        </div>
        <div class="url">
            <span style="color:#4fdd48;">{url}</span>
        </div>
        """ 
        if not "AboutPressCopyrightContact" in description:
            s += ("<div class=description>" + description + "</div>")
        
        return  s;

    def generate_html_for_token(self, tag : str, content : str) -> str:
        # Generates HTML based on the tag, content, and url (for links)
        if tag == "text":
            # Return plain text content for text tags
            return " " + content
        elif tag == "link":
            return " " + content
            # Generate a span with a style for color-coded content
            # Format the content for the URL query string
            #  query_content = content.replace("."," ").replace("  "," ").replace(" ", "+")
            #  return f'<a href="?q={query_content}" style="color:blue;" target="_self">{content}</a>'
        else:
            # Default case returns content as is
            return f'<span style="color:red;">{content}</span>'

    def generate_html_for_answer(self, oText:Text) -> str:
        # Generates HTML for all tokens in the list, using url for links
        formatted_tokens = [self.generate_html_for_token(tag, content) for (tag, content) in oText.tokens]
        s = " ".join(formatted_tokens)
        s = s.replace("\n\n", "<br />")

        return s

    def generate_html_for_results(self, LIMIT : int = 7) -> str:
        # Generates HTML for all tokens in the list

        urls = []   # to avoid the repetition of links

        results = self.agent.results

        result_html = ""
        for result in results:
            url : str = result["url"]

            if not url in urls:
                html : str = self.generate_html_for_result(result)
                result_html += html + "<br>"
                urls.append(url)
                if len(urls) >= LIMIT:
                    break;

        return  result_html

    def render_user_message(self, message):
        html = f"""
        <div style='text-align: right;'>
            <span style='margin-left:200px; color: white; background-color: blue; padding: 10px; border-radius: 5px;'>{message}</span>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    def render_chatbot_message(self, generated_content : str):
        st.markdown(self.generate_html_for_answer(oText=oText), unsafe_allow_html=True)
        st.markdown("<br />", unsafe_allow_html=True)
        oText = Text(generated_content = generated_content, concepts = self.agent.concepts)
        st.markdown(self.generate_html_for_results(), unsafe_allow_html=True)
        st.markdown("<br />", unsafe_allow_html=True)

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
    # and display them in the chat message container ?
    def render_messages(self):
        st.sidebar.write("")
        st.sidebar.write(self.agent.start)

        for message_object in self.agent.messages:
            self.render_message(message_object)

