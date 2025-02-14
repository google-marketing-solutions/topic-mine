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
import re
import time
import vertexai

import dirtyjson
import google.generativeai as genai
from prompts.prompts import prompts
from vertexai.generative_models import GenerativeModel, SafetySetting

# Logger config
logging.basicConfig()
logging.root.setLevel(logging.INFO)

RETRIES = 5
GENERATION_CONFIG = {
    'temperature': 1,
    'max_output_tokens': 8192,
    'top_p': 0.95,
}
SAFETY_SETTINGS = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]

TIME_INTERVAL_BETWEEN_REQUESTS = 0
TIME_INTERVAL_IF_QUOTA_ERROR = 60
TIME_INTERVAL_IF_GEMINI_ERROR = 10


class GeminiHelper:
  """Gemini helper to perform Gemini API requests.
  """

  def __init__(self, config: dict[str, str]) -> None:
    self.config = config

    if 'gemini_model' in config and config["gemini_model"]:
      model_name = config['gemini_model']
      models = ['gemini-1.5-flash', 'gemini-1.5-flash-8b', 'gemini-1.5-pro']
      if model_name not in models:
        model_name = 'gemini-1.5-flash'
    else:
      model_name = 'gemini-1.5-flash'

    if 'gemini_api_key' in config and config["gemini_api_key"]:
      key = config['gemini_api_key']
      genai.configure(api_key=key)
      self.model = genai.GenerativeModel(model_name)
    else:
      vertexai.init(project=config['project_id'], location='us-central1')
      self.model = GenerativeModel(model_name)

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
            generation_config=GENERATION_CONFIG,
            safety_settings=SAFETY_SETTINGS
            )
        response_json = re.search('({.*?})', response.text, re.DOTALL).group(1)
        response_json = dirtyjson.loads(response_json)
        response_json = dict(response_json)
        time.sleep(TIME_INTERVAL_BETWEEN_REQUESTS)

        return response_json
      except Exception as e:
        if 'Quota exceeded' in str(e) or 'quota' in str(e).lower():
          logging.error(
              'Quota exceeded, sleeping %ds. Retries left: %d...',
              TIME_INTERVAL_IF_QUOTA_ERROR,
              retries
              )
          time.sleep(TIME_INTERVAL_IF_QUOTA_ERROR)
        elif ('candidate' in str(e) or 'response was blocked' in str(e)
              or 'quick accessor' in str(e)):
          logging.error(
              'Gemini error, sleeping %ds. Retries left: %d...',
              TIME_INTERVAL_IF_GEMINI_ERROR,
              retries
              )
          time.sleep(TIME_INTERVAL_IF_GEMINI_ERROR)
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
            generation_config=GENERATION_CONFIG,
            safety_settings=SAFETY_SETTINGS
            )
        start_idx = response.text.index('[')
        end_idx = response.text.index(']')
        time.sleep(TIME_INTERVAL_BETWEEN_REQUESTS)

        return ast.literal_eval(response.text[start_idx:end_idx+1])
      except Exception as e:
        if 'Quota exceeded' in str(e) or 'quota' in str(e).lower():
          logging.error(
              'Quota exceeded, sleeping %ds. Retries left: %d...',
              TIME_INTERVAL_IF_QUOTA_ERROR,
              retries
              )
          time.sleep(TIME_INTERVAL_IF_QUOTA_ERROR)
        elif ('candidate' in str(e) or 'response was blocked' in str(e)
              or 'quick accessor' in str(e)):
          logging.error(
              'Gemini error, sleeping %ds. Retries left: %d...',
              TIME_INTERVAL_IF_GEMINI_ERROR,
              retries
              )
          time.sleep(TIME_INTERVAL_IF_GEMINI_ERROR)
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
            generation_config=GENERATION_CONFIG,
            safety_settings=SAFETY_SETTINGS
            )
        time.sleep(TIME_INTERVAL_BETWEEN_REQUESTS)

        return response.text
      except Exception as e:
        if 'Quota exceeded' in str(e) or 'quota' in str(e).lower():
          logging.error(
              'Quota exceeded, sleeping %ds. Retries left: %d...',
              TIME_INTERVAL_IF_QUOTA_ERROR,
              retries
              )
          time.sleep(TIME_INTERVAL_IF_QUOTA_ERROR)
        elif ('candidate' in str(e) or 'response was blocked' in str(e)
              or 'quick accessor' in str(e)):
          logging.error(
              'Gemini error, sleeping %ds. Retries left: %d...',
              TIME_INTERVAL_IF_GEMINI_ERROR,
              retries
              )
          time.sleep(TIME_INTERVAL_IF_GEMINI_ERROR)
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
    if copy == 'Generation error':
      return copy

    if t == 'headlines':
      max_length = 30
    elif t == 'descriptions':
      max_length = 90
    elif t == 'paths':
      max_length = 15
    else:
      message = f"Unsupported val: {t}. Supported: 'headlines', 'descriptions', 'paths'"
      raise ValueError(message)

    if retries == 0:
      return 'Review: ' + copy
    else:
      prompt = self.__get_enforce_size_prompt(copy, t)

      result = self.run_prompt(prompt)

      result = result.strip() if result is not None else None

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
    elif t == 'paths':
      max_length = 15
    else:
      message = f"Unsupported val: {t}. Supported: 'headlines', 'descriptions', 'paths'"
      raise ValueError(message)

    if t == 'paths':
      return prompts[self.config['language']]['PATH_SIZE_ENFORCEMENT'].format(
          max_length=max_length,
          copy=copy,
          )

    return prompts[self.config['language']]['SIZE_ENFORCEMENT'].format(
        max_length=max_length,
        copy=copy,
        )
