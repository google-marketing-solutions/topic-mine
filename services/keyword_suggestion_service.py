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

"""Keyword Suggestion service.

This module contains all the methods for
generating keyword suggestions using the Google Ads API.
"""

import logging
import time

from google.ads.googleads.client import GoogleAdsClient
from utils.authentication_helper import Authenticator

# Logger config
logging.basicConfig()
logging.root.setLevel(logging.INFO)


class KeywordSuggestionService():
  """A service for generating keyword suggestions using the Google Ads API.
  """

  def __init__(self, config: dict[str, str]):
    """Initialize a KeywordSuggestionService instance.

    Args:
      config (dict[str, str]): A dictionary containing configuration parameters.
    """
    authenticator = Authenticator()
    self.creds = authenticator.authenticate_with_client_credentials(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        refresh_token=config['refresh_token'],
        )
    self.config = config
    self.client = GoogleAdsClient(
        self.creds,
        self.config['google_ads_developer_token'],
        login_customer_id=self.config['login_customer_id']
        )

  def get_keywords(self, terms) -> list[str]:
    """Retrieve keyword suggestions for a list of terms.

    Args:
      terms (list[str]): A list of terms for which you want keyword suggestions.

    Returns:
      list[str]: A list of keyword suggestions.
    """
    customer_id = self.config['login_customer_id']

    location_ids = {
        'Argentina': '2032',
        'Chile': '2152',
        'Colombia': '2170',
        'Mexico': '2484',
        'Peru': '2604',

        'Brazil': '2076',

        'Canada': '2124',
        'United States': '2840'
        }

    if self.config['language'] == 'ES':
      language_id = '1003'  # ES
      location_id = '2484'  # MX, default value if language is ES
    elif self.config['language'] == 'EN':
      language_id = '1000'  # EN
      location_id = '2840'  # US, default value if language is EN
    elif self.config['language'] == 'PT':
      language_id = '1014'  # PT
      location_id = '2076'  # BR, default value if language is PT
    else:
      raise ValueError(f'Language {self.config["language"]} not supported')

    if (
        self.config['country'] is not None and
        self.config['country'].capitalize() in location_ids
        ):
      location_id = location_ids[self.config['country']]

    try:
      for _ in range(5):
        try:
          client = self.client
          keyword_plan_idea_service = client.get_service(
              'KeywordPlanIdeaService'
              )

          keyword_plan_network = (
              client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH_AND_PARTNERS
              )
          location_rns = self.__map_locations_ids_to_resource_names(
              [location_id]
              )
          language_rn = (
              client.get_service('GoogleAdsService').language_constant_path(
                  language_id
                  )
              )

          request = client.get_type('GenerateKeywordIdeasRequest')

          request.customer_id = customer_id
          request.language = language_rn

          request.geo_target_constants.extend(location_rns)
          request.include_adult_keywords = False
          request.keyword_plan_network = keyword_plan_network

          # To generate kwrd ideas with only a list of keywords and no page_url
          # we need to initialize a KeywordSeed obj and set 'keywords' field
          # to be a list of StringValue objects.
          request.keyword_seed.keywords.extend(terms)
          keyword_ideas = keyword_plan_idea_service.generate_keyword_ideas(
              request=request
              )

          list_of_ideas = []

          for idea in keyword_ideas:
            list_of_ideas.append(idea.text)

          return list_of_ideas[:10]
        except Exception as e:
          if 'Quota exceeded' in str(e) or 'quota' in str(e).lower():
            time.sleep(70)
          continue
    except Exception as e:
      logging.error(' Error in get_keywords: %s', str(e))

    return[]

  def __map_locations_ids_to_resource_names(self, location_ids) -> list[str]:
    """Converts a list of location IDs to resource names.

    Args:
      location_ids (list): a list of location ID strings.

    Returns:
      list[str]: a list of resource name strings using the given location IDs.
    """
    build_resource_name = self.client.get_service(
        'GeoTargetConstantService'
        ).geo_target_constant_path

    return [build_resource_name(location_id) for location_id in location_ids]
