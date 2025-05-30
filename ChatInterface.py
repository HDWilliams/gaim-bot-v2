"""
Class for creating the chat interface, setting session variables and calling aws lambda backend
"""

import streamlit as st
from typing import Literal
from AWSLambdaInterface import LambdaChatInterface

class ChatInterface:
    """Handles establishing chat session and relevant state variables

    Methods:
        add_message_to_state
        add_state_messages_to_chat
        update_chat_messages
        _create_lambda_interface
        create_chat_interface



    """
    def __init__(self, starter_message:str ) -> None:
        if 'messages' not in st.session_state:
            self.add_message_to_state('assistant', starter_message)
        if 'instructions' not in st.session_state:
            st.session_state['instructions'] = {'role': 'developer', 'content': st.secrets['INSTRUCTIONS']}
   
    def enable_chat(self) -> None:
        """Helper function for setting variable to False, allowing use to interact with chat

        Args: None
        Returns: None

        """
        st.session_state['disabled_chat'] = False
    
    def disable_chat(self) -> None:
        """Helper function for setting variable to True, disallow user to interact with chat while waiting for response

        Args: None
        Returns: None

        """
        st.session_state['disabled_chat'] = True
    
    def add_message_to_state(self, role: str | Literal['assistant', 'user'], content:str) -> None:
        message = {'role': role, 'content': content}
        if 'messages' not in st.session_state:
            st.session_state['messages'] = [message]
        else:
            st.session_state['messages'].append(message)
    
    def add_state_messages_to_chat(self) -> None:
        """Write messages saved in state to the chat object to display to user

        Args: None
        Returns: None

        """

        # Do not include the initial system message, only to send to backend
        for message in st.session_state['messages']:
            st.chat_message(message['role']).write(message['content'])
    
    def update_chat_messages(self, role:str | Literal['assistant', 'user'], content:str) -> None:
        """Add message to end of List of messages

        Args: 
            role: Literal['assistant', 'user']
        Returns: None

        """
        st.chat_message(role).write(content)
    
    def _create_lambda_interface(self, api_key:str, url:str) -> LambdaChatInterface:
        """Returns LambdaChatInterface object with stored api key information, for calling backend ai responses

        Args: 
            api_key: str
            url: str
        Returns: LambdaChatInterface

        """
        if 'chat_interface' not in st.session_state:
            st.session_state['chat_interface'] = LambdaChatInterface(api_key, url)
        return st.session_state['chat_interface']


    def create_chat_interface(self) -> None:
        """Creates chats session for user interaction. 
        Handles storing, displaying user messages and post request for ai chat completion.

        Args: 
            api_key: str
            url: str
        Returns: None

        """
        self._create_lambda_interface(st.secrets['LAMBDA_API_KEY'], st.secrets['LAMBDA_GPT_URL'])
       
        self.add_state_messages_to_chat()
        self.enable_chat()

        if query := st.chat_input(max_chars=250, disabled=st.session_state["disabled_chat"]):
            # Accept input from user
            if not st.session_state["disabled_chat"]:


                # Add the user message to the chat log and message history
                self.disable_chat()
                self.add_message_to_state('user', query)
                st.chat_message("user").write(query)


                # Get chat completion from lambda function. TODO implement response streaming
                lambda_chat_interface: LambdaChatInterface = st.session_state['chat_interface']
                content = lambda_chat_interface.get_gpt_chat_response(st.session_state['messages'])

                self.add_message_to_state('assistant', content)
                st.chat_message("assistant").write(content)

            self.enable_chat()
