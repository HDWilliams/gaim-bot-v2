import streamlit as st
from typing import Literal
import requests
from AWSLambdaInterface import LambdaChatInterface

class ChatInterface:
    def __init__(self, starter_message:str ) -> None:
        self.enable_chat()
        if 'messages' not in st.session_state:
            self.add_message_to_state('assistant', starter_message)
   
    def enable_chat(self) -> None:
        st.session_state['disabled_chat'] = False
    
    def add_message_to_state(self, role: str | Literal['assistant', 'user'], content:str) -> None:
        message = {'role': role, 'content': content}
        if 'messages' not in st.session_state:
            st.session_state['messages'] = [message]
        else:
            st.session_state['messages'].append(message)
    
    def add_state_messages_to_chat(self) -> None:
        for message in st.session_state['messages']:
            st.chat_message(message['role']).write(message['content'])
    
    def update_chat_messages(self, role:str | Literal['assistant', 'user'], content:str) -> None:
        st.chat_message(role).write(content)
    
    def _create_lambda_interface(self, api_key, url) -> LambdaChatInterface:
        if 'chat_interface' not in st.session_state:
            st.session_state['chat_interface'] = LambdaChatInterface(api_key, url)
        return st.session_state['chat_interface']


    def create_chat_interface(self):
        """
        client: streamlit client object
        conversation_thread: gpt conversation thread
        conversation_assistant: gpt conversation assistant object
        get_research: function from Research object to allow gpt research model to get info for conversational model

        returns None
        
        """
        self._create_lambda_interface(st.secrets['LAMBDA_API_KEY'], st.secrets['LAMBDA_GPT_URL'])
       
        self.add_state_messages_to_chat()

        if query := st.chat_input(max_chars=250, disabled=st.session_state["disabled_chat"]):
            #DISABLE USER INPUT WHILE WAITING FOR MESSAGE
            if not st.session_state["disabled_chat"]:


                #ADD USER MESSAGE TO MESSAGE LIST
                self.add_message_to_state('user', query)
                st.chat_message("user").write(query)


                # Temp variable
                chat_interface: LambdaChatInterface = st.session_state['chat_interface']
                content = chat_interface.get_gpt_chat_response(st.session_state['messages'])

                self.add_message_to_state('assistant', content)
                st.chat_message("assistant").write(content)
            self.enable_chat()