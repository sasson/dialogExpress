import streamlit as st
from dialog_page import DialogPage
from channel_definition import ChannelDefinition

# base_url = "https://sasson-dialogexpress-app-jkbb2w.streamlit.app"

definitions = ChannelDefinition.read_all(file_path = "channels.toml")

query_params = st.experimental_get_query_params()
# [""] is a fallback value if the parameter isn't found
name = query_params.get('ch', [""]) [0]
q = query_params.get('q', [""]) [0]

if not name:
    name = "general"

if name in definitions:
    definition = definitions[name]

    # Create an instance of DialogPage
    page = DialogPage(definition = definition, q = q)
    st.session_state.page = page

    # Display channel name and domain in the sidebar
    if isinstance(page.name, str):
        st.sidebar.title(page.name)

    page.render_messages()

    # check if user made a chat input
    input_text = st.chat_input("Say something", key="chat_input")
    if input_text:    
        page.on_input(input_text = input_text)

else:
    st.write (name + " is not one of channels specified in 'channels.toml'")
