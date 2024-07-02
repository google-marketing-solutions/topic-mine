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

"""Gemini Helper.
"""

import ast
import logging
import os
import re
import time

import dirtyjson
import google.generativeai as genai
from prompts.prompts import prompts

# Logger config
logging.basicConfig()
logging.root.setLevel(logging.INFO)

RETRIES = 5
GENERATION_CONFIG = {
    'temperature': 0.6,
    'max_output_tokens': 1024,
    'top_p': 0.8,
    'top_k': 40
}
TIME_INTERVAL = 0.3


class GeminiHelper:
  """Gemini helper to perform Gemini API requests.
  """

  def __init__(self, config: dict[str, str]) -> None:
    self.config = config

    try:
      key = os.environ['API_KEY']
    except KeyError:
      key = config['gemini_api_key']
    genai.configure(api_key=key)
    self.model = genai.GenerativeModel('gemini-1.5-pro')

  def generate_dict(self, prompt: str) -> dict:
    """Makes a request to Gemini and returns a dict.

    Args:
      prompt (str): The prompt to ask Gemini to generate content

    Returns:
      dict: Response dict.
    """
    retries = RETRIES
    while retries > 0:
      try:
        response = self.model.generate_content(
            prompt,
            generation_config=GENERATION_CONFIG
            )
        response_json = re.search('({.*?})', response.text, re.DOTALL).group(1)
        response_json = dirtyjson.loads(response_json)
        response_json = dict(response_json)
        time.sleep(TIME_INTERVAL)

        return response_json
      except Exception as e:
        if 'Quota exceeded' in str(e) or 'quota' in str(e).lower():
          logging.error(
              'Quota exceeded, sleeping 60s. Retries left: %d...',
              retries
              )
          time.sleep(60)
        elif ('candidate' in str(e) or 'response was blocked' in str(e)
              or 'quick accessor' in str(e)):
          logging.error(' Gemini error. Retries left: %d...', retries)
        else:
          logging.error(' %s. Retries left: %d...', str(e), retries)
      retries = retries - 1
    return {'status': 'Error'}

  def generate_text_list(self, prompt: str) -> list[str]:
    """Makes a request to Gemini and returns a list of strings.

    Args:
      prompt (str): the prompt to ask Gemini to generate content

    Returns:
      list[str]: a list of strings with the generated texts
    """
    retries = RETRIES
    while retries > 0:
      try:
        response = self.model.generate_content(
            prompt,
            generation_config=GENERATION_CONFIG
            )
        start_idx = response.text.index('[')
        end_idx = response.text.index(']')
        time.sleep(TIME_INTERVAL)

        return ast.literal_eval(response.text[start_idx:end_idx+1])
      except Exception as e:
        if 'Quota exceeded' in str(e) or 'quota' in str(e).lower():
          logging.error(
              'Quota exceeded, sleeping 60s. Retries left: %d...',
              retries
              )
          time.sleep(60)
        elif ('candidate' in str(e) or 'response was blocked' in str(e)
              or 'quick accessor' in str(e)):
          logging.error(' Gemini error. Retries left: %d...', retries)
        else:
          logging.error(' %s. Retries left: %d...', str(e), retries)
      retries = retries - 1
    return ['Generation failed']

  def run_prompt(self, prompt: str) -> str:
    """Makes a request to Gemini and returns a the response.

    Args:
      prompt (str): the prompt to ask Gemini to generate content

    Returns:
      response (str): response
    """
    retries = RETRIES
    while retries > 0:
      try:
        response = self.model.generate_content(
            prompt,
            generation_config=GENERATION_CONFIG
            )
        time.sleep(TIME_INTERVAL)

        return response.text
      except Exception as e:
        if 'Quota exceeded' in str(e) or 'quota' in str(e).lower():
          logging.error(
              'Quota exceeded, sleeping 60s. Retries left: %d...',
              retries
              )
          time.sleep(60)
        elif ('candidate' in str(e) or 'response was blocked' in str(e)
              or 'quick accessor' in str(e)):
          logging.error(' Gemini error. Retries left: %d...', retries)
        else:
          logging.error(' %s. Retries left: %d...', str(e), retries)
      retries = retries - 1
    return None

  def enforce_text_size(self, copy: str, t: str, retries: int = RETRIES) -> str:
    """Enforces size limits on generated content of a specified type.

    Args:
      copy (str): The generated content to be checked and potentially resized.
      t (str): The type of content ('headlines', 'descriptions', etc.).
      retries (int, optional): The number of retry attempts (default is 5).

    Returns:
      str: The resized content that meets the size limits.

    Raises:
      ValueError: If the specified type is not supported.
    """
    if t == 'headlines':
      max_length = 30
    elif t == 'descriptions':
      max_length = 90
    else:
      message = f"Unsupported val: {t}. Supported: 'headlines', 'descriptions'"
      raise ValueError(message)

    if retries == 0:
      return 'Review: ' + copy
    else:
      prompt = self.__get_enforce_size_prompt(copy, t)

      result = self.run_prompt(prompt)

      if result is None or len(result) > max_length:
        return self.enforce_text_size(result, t, retries-1)
      else:
        return result

  def __get_enforce_size_prompt(self, copy: str, t: str) -> str:
    """Generates a text prompt enforcing copy sizes.

    Args:
      copy (str): The copy that is too long.
      t (str): The type (headlines|descriptions).

    Returns:
      str: A text prompt for shortening the copy.

    Raises:
      ValueError: If the specified type is not supported.
    """
    if t == 'headlines':
      max_length = 30
    elif t == 'descriptions':
      max_length = 90
    else:
      message = f"Unsupported val: {t}. Supported: 'headlines', 'descriptions'"
      raise ValueError(message)

    return prompts[self.config['language']]['SIZE_ENFORCEMENT'].format(
        max_length=max_length,
        copy=copy,
        )
