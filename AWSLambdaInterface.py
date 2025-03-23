import streamlit as st
import requests
from dataclasses import dataclass
from typing import List
import tenacity
import ratelimit



class LambdaChatInterface:
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
        print(f'Retrying: {retry_state.attempt_number}. Exception Info: {retry_state.outcome.exception()}')

    # Add in logic to catch more specific errors
    @tenacity.retry(
            wait=tenacity.wait_exponential_jitter(max=15),
            stop=tenacity.stop_after_attempt(3),
            retry=tenacity.retry_if_exception_type(requests.exceptions.RequestException),
            before_sleep=log_retry
    )
    def get_gpt_chat_response(self, messages:List[dict], timeout=30) -> str:


        # Exclude the intro message to the user
        messages_with_instructions = st.session_state['instructions'] + messages[1:]

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