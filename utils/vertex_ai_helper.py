# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import vertexai
from vertexai.preview.language_models import TextGenerationModel
import re
import dirtyjson
from utils.authentication_helper import Authenticator
from google.auth.transport.requests import Request
import logging
import ast

# Logger config
logging.basicConfig()
logging.root.setLevel(logging.INFO)

MODEL_NAME = "chat-bison@001"
TEMPERATURE = 0
MAX_OUTPUT_TOKENS = 1024
TOP_P = 0.8
TOP_K = 40
TEXT_MODEL_NAME="text-bison@001"
RETRIES=5
PARAMETERS = {
    'temperature': 0.3,
    'max_output_tokens': 1024,
    'top_p': 0.8,
    'top_k': 40
}


class VertexAIHelper:
    """Vertex AI helper to leverage the PaLM API chat"""

    def __init__(self, config):
        self.config = config
        self.location = config["project_region"]
        self.project_id = config["project_id"]
        authenticator = Authenticator()
        self.creds = authenticator.authenticate_with_client_credentials(
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            refresh_token=config["refresh_token"],
        )
        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
        vertexai.init(project = self.project_id, location = self.location, credentials = self.creds)
        self.model = TextGenerationModel.from_pretrained(TEXT_MODEL_NAME)

    def generate_text_content_with_palm(self, prompt: str):
        """ Makes an API request to the PaLM API to generate text content

        Args:
            prompt (str): the prompt to ask PaLM to generate content

        Returns:
            response (Any): either a JSON or a string
        """
        retries = RETRIES
        while retries > 0:
            # Try to load a simple JSON response
            try:
                response = self.model.predict(prompt, **PARAMETERS)
                response_json = re.search("({.*?})", response.text, re.DOTALL).group(1)
                response_json=dirtyjson.loads(response_json)
                response_json=dict(response_json)
                return response_json
            except Exception as e:
                print(f'ERROR: {e}. Response could not be parsed. Trying again {retries}...')
            # If it didn't work with a simple JSON load, try the call again
            retries = retries - 1
        # If no match, just return the response
        return response.text


    def generate_text_list_with_palm(self, prompt: str) -> list:
        """ Makes an API request to the PaLM API to generate text content and returns a list of elements

        Args:
            prompt (str): the prompt to ask PaLM to generate content

        Returns:
            response (list): a list of strings
        """
        retries = RETRIES
        while retries > 0:
            try:
                response = self.model.predict(prompt, **PARAMETERS)
                return ast.literal_eval(response.text)
            except Exception as e:
                logging.error(f'ERROR: {e}')
            retries = retries - 1
        return response.text


    def run_prompt(self, prompt: str) -> str:
        """ Makes an API request to the PaLM API to generate text content and returns the response

        Args:
            prompt (str): the prompt to ask PaLM to generate content

        Returns:
            response (str): response
        """
        retries = RETRIES
        while retries > 0:
            try:
                response = self.model.predict(prompt, **PARAMETERS)
                return response.text
            except Exception as e:
                logging.error(f'Error running prompt: {str(e)}')
            retries = retries - 1
        return None
