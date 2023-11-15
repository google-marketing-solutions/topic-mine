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

from google.ads.googleads.client import GoogleAdsClient
import time
from utils.authentication_helper import Authenticator

class KeywordSuggestionService():
    """
    A service for generating keyword suggestions using the Google Ads API.
    """

    def __init__(self, config):
        """
        Initialize a KeywordSuggestionService instance.

        Args:
        - config (dict): A dictionary containing configuration parameters.
        """
        authenticator = Authenticator()
        self.creds = authenticator.authenticate_with_client_credentials(
            client_id = config["client_id"],
            client_secret = config["client_secret"],
            refresh_token = config["refresh_token"],
        )
        self.config = config
        self.client = GoogleAdsClient(self.creds, self.config["dev_token"], login_customer_id = self.config["login_customer_id"])


    def get_keywords(self, terms):
        """
        Retrieve keyword suggestions for a list of terms.

        Args:
        - terms (list of str): A list of terms for which you want keyword suggestions.

        Returns:
        - list of str: A list of keyword suggestions.
        """
        customer_id = self.config["login_customer_id"]
        location_ids = self.config['keywords']['region_codes']
        language_id = self.config['keywords']['language_code']
        try:

            for c in range(5):
                try:

                    client = self.client
                    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")

                    keyword_plan_network = (
                        client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH_AND_PARTNERS
                    )
                    location_rns = self.map_locations_ids_to_resource_names(location_ids)
                    language_rn = client.get_service("GoogleAdsService").language_constant_path(
                        language_id
                    )

                    request = client.get_type("GenerateKeywordIdeasRequest")

                    request.customer_id = customer_id
                    request.language = language_rn

                    request.geo_target_constants.extend(location_rns)
                    request.include_adult_keywords = False
                    request.keyword_plan_network = keyword_plan_network

                    # To generate keyword ideas with only a list of keywords and no page_url
                    # we need to initialize a KeywordSeed object and set the "keywords" field
                    # to be a list of StringValue objects.
                    request.keyword_seed.keywords.extend(terms)
                    keyword_ideas = keyword_plan_idea_service.generate_keyword_ideas(
                        request=request
                    )
                    list_of_ideas=[]

                    for idea in keyword_ideas:
                        list_of_ideas.append(idea.text)

                    return list_of_ideas[:10]
                except:
                    print("Error in keywords suggestion")
                    print(str(c))
                    time.sleep(60)
                    print("1 minute has passed")
                    continue
        except:
            print("Total error suggestion returning []")
            return []
        print("Finally returning[]")
        return[]


    def map_locations_ids_to_resource_names(self, location_ids):
        """Converts a list of location IDs to resource names.
        
        Args:
        - location_ids (list of str): a list of location ID strings.

        Returns:
        - a list of resource name strings using the given location IDs.
        """
        build_resource_name = self.client.get_service(
            "GeoTargetConstantService"
        ).geo_target_constant_path

        return [build_resource_name(location_id) for location_id in location_ids]
