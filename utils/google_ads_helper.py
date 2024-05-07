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

"""Google Ads Helper.

This module contains the Google Ads helper class.
"""

from google.auth.transport.requests import Request
from services.keyword_suggestion_service import KeywordSuggestionService
from utils.authentication_helper import Authenticator


class GoogleAdsHelper:
  """Google Ads helper to interact with the service using the specified client.
  """

  def __init__(self, config: dict[str, str]) -> None:
    """Initialize a GoogleAdsHelper instance.

    Args:
      config (dict[str, str]): A dictionary containing configuration parameters.
    """
    self.config = config
    authenticator = Authenticator()
    self.creds = authenticator.authenticate_with_client_credentials(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        refresh_token=config['refresh_token'],
        )
    if self.creds and self.creds.expired and self.creds.refresh_token:
      self.creds.refresh(Request())

  def get_keywords_suggestions(self, terms: list[str]) -> list[str]:
    """Get keyword suggestions for a list of terms.

    Args:
      terms (list[str]): A list of terms for which you want
      keyword suggestions.

    Returns:
      list[str]: A list of suggestions for each term in terms.
    """
    keyword_suggestion_service = KeywordSuggestionService(self.config)

    suggestions = (
        [keyword_suggestion_service.get_keywords([term]) for term in terms])

    str_values = [(
        '[' + ', '.join(f'"{keyword}"' for keyword in keywords_per_term) + ']'
        for keywords_per_term in suggestions
        )]

    return str_values
