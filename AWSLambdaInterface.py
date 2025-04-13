"""
Class containing functions for interacting with AWS lambda retrieval + chat completion function

"""
import json
import streamlit as st
import requests, asyncio
from typing import List
import tenacity
import ratelimit



class LambdaChatInterface:
    """Handles establishing interaction with lambda retrieval and chat function

    Methods:
        log_retry(retry_state)
        get_gpt_chat_response(messages, timeout)


    """
    def __init__(self, api_key: str, url:str, content_type:str = 'application/json', model='gpt-4o-mini') -> None:
        self.headers = {
            'content-type': content_type,
            'x-api-key': api_key
        }
        self.url = url
        self.model = model

    # Add proper logging
    @staticmethod
    def log_retry(retry_state: tenacity.RetryCallState) -> None:
        """Logging errors when tenacity encounters retry error

        Args: 
            retry_state: tenacity.RetryCallState
        Returns: None
        """
        print(f'Retrying: {retry_state.attempt_number}. Exception Info: {retry_state.outcome.exception()}')

    # TODO: specify additional exceptions to catch that are more specific, HttpException, ConnectionError, Ratelimit etc.
    @tenacity.retry(
            wait=tenacity.wait_exponential_jitter(max=15),
            stop=tenacity.stop_after_attempt(3),
            retry=tenacity.retry_if_exception_type(requests.exceptions.RequestException),
            before_sleep=log_retry
    )
    def get_gpt_chat_response(self, messages:List[dict], timeout=30) -> str:
        """Query backend lambda function for API response. Returns ai generated response as a string

        Args: 
            messages: List[{'role': Literal['assistant', 'user', 'developer'], 'content': str}]
            timeout: int, time for request to timeout

        Returns: str
        """

        # Exclude the intro message to the user
        messages_with_instructions = [st.session_state['instructions']] + messages[1:]

        body = {
            "model": self.model,
            "messages": messages_with_instructions,
            "index_name": st.secrets['INDEX_NAME']
        }

        try:
            with st.spinner("I'm thinking...", show_time=False):
                response = requests.post(self.url, headers=self.headers, json=body, timeout=timeout)
                response.raise_for_status()


                # Need to catch json decode error
                response_json = response.json()

                return response_json['data']
        except tenacity.RetryError as e:
            print(f'Retry Error {e}.')
            return 'Sorry I seem to have experienced an error'
        
    def stream_gpt_chat_response(self, messages:List[dict], timeout=30) -> str:
        """Query backend lambda function for API response. Returns ai generated response as a string

        Args: 
            messages: List[{'role': Literal['assistant', 'user', 'developer'], 'content': str}]
            timeout: int, time for request to timeout

        Returns: str
        """

        # Exclude the intro message to the user
        messages_with_instructions = [st.session_state['instructions']] + messages[1:]

        body = {
            "model": self.model,
            "messages": messages_with_instructions,
            "index_name": st.secrets['INDEX_NAME']
        }

        try:
            with st.spinner("I'm thinking...", show_time=False):
                response = requests.post(self.url, headers=self.headers, json=body, timeout=timeout)
                response.raise_for_status()


                # Need to catch json decode error
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        print(line)
                        chunk = json.loads(line)
                        if isinstance(chunk, dict):
                            yield chunk['error']
                            return
                        yield chunk
        except tenacity.RetryError as e:
            print(f'Retry Error {e}.')
            return 'Sorry I seem to have experienced an error'