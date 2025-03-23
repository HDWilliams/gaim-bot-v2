import streamlit as st
from ChatInterface import ChatInterface

if 'chat' not in st.session_state:
    st.session_state['chat'] = ChatInterface(st.secrets['INITIAL_MESSAGE'])
st.session_state['chat'].create_chat_interface()