import streamlit as st

def main():
    # Set page layout
    st.set_page_config(layout="wide")

    # Define left pane 
    left_column = st.sidebar
    left_column.title(" ")

    # Define main area AND sticky footer
    main_area = st.container()
    with main_area:
        st.write("This is the main area") 
        st.write("")

        # Add sticky footer
        st.markdown('<div style="position: fixed; bottom: 0; width: 100%; background-color: lightgray; padding: 10px;">', unsafe_allow_html=True)
        search_query = st.text_input("Search")
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
