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

from utils.authentication_helper import Authenticator
from utils.vertex_ai_helper import VertexAIHelper
from utils.bigquery_helper import BigQueryHelper
from utils.sheet_helper import GoogleSheetsHelper
from utils.utils import Utils
from services.keyword_suggestion_service import KeywordSuggestionService
import logging
import pandas as pd
from itertools import product
from flask import jsonify
from prompts.prompts import prompts
import time
from alive_progress import alive_bar

# Logger config
logging.basicConfig()
logging.root.setLevel(logging.INFO)

RETRIES = 3

class GoogleTrendsService:
    """
    This class contains methods for generating copies related with google trending topics and brands matching actions.
    """
    def __init__(self, config):
        authenticator = Authenticator()
        self.creds = authenticator.authenticate_with_client_credentials(
            client_id = config["client_id"],
            client_secret = config["client_secret"],
            refresh_token = config["refresh_token"],
        )
        self.config = config


    def start(self) -> None:
        """
        Entry point for this service. Starts the copy generation process associated with google trends.
        Generates headlines and descriptions.

        Returns:
        - tuple: Tuple with success message and code
        """
        logging.info('Starting google trends content generation from GoogleTrendsService.start method')

        sheet_helper = GoogleSheetsHelper(self.config)
        bigquery_helper = BigQueryHelper(self.config)
        vertex_ai_helper = VertexAIHelper(self.config)
        keyword_suggestion_service = KeywordSuggestionService(self.config)

        # Get top terms from the public Google trends dataset in BQ
        logging.info(f'Getting google trends from BigQuery')
        trends = bigquery_helper.google_trends_get_trends_from_bq(self.config['google_trends']['big_query']['trends_params'])

        # Get the brands from either Google Merchant Center or a provided list in the self.config
        if self.config['google_trends']['brand_params']['merchant_center']:
            logging.info(f'Getting brands from Merchant center')
            brands = bigquery_helper.get_brands_from_merchant_center()
        else:
            logging.info(f'Getting brands from config')
            brands = self.config['google_trends']['brand_params']['brands']

        international = self.config['google_trends']['big_query']['trends_params']['international']

        combinations = list(product(trends.keys(), brands))

        # Create a Pandas DataFrame from the combinations
        df = pd.DataFrame(combinations, columns=['Trend', 'Brand'])

        with alive_bar(len(df) + 2) as bar:
            for index, row in df.iterrows():
                trends_info = trends[row['Trend']]
                prompt = self.__get_trend_association_prompt(row['Trend'], row['Brand'], trends_info['country_name'] if international else trends_info['dma_name'])
                logging.info(f'Getting association info between {row["Trend"]} and {row["Brand"]}')
                response = vertex_ai_helper.generate_text_content_with_palm(prompt)
                logging.info(f'Relationship: {response["relationship"]} - {response["reason"]}')
                df.at[index, 'ID'] = '{0}'.format(response['trend'].replace(' ', '_'))

                if isinstance(response, dict):                
                    df.at[index, 'Country code'] = trends_info['country_code'] if international else trends_info['dma_id']
                    df.at[index, 'Country name'] = trends_info['country_name'] if international else trends_info['dma_name']
                    df.at[index, 'Week'] = str(trends_info['week'])
                    df.at[index, 'Rank'] = str(trends_info['rank'])
                    df.at[index, 'Score'] = str(trends_info['score'])
                    df.at[index, 'Refresh date'] = str(trends_info['refresh_date'])
                    df.at[index, 'Suggested ad name'] = '{0}_{1}_Trendy_Google'.format(row['Trend'].replace(' ', ''), row['Brand'].replace(' ', ''))
                    df.at[index, 'Relationship'] = response["relationship"]
                    df.at[index, 'Reason'] = response["reason"]

                    if response["relationship"]:
                        df.at[index, 'Generated headlines'] = self.__generate_headlines(row['Trend'], row['Brand'], response["reason"])
                        df.at[index, 'Generated descriptions'] = self.__generate_descriptions(row['Trend'], row['Brand'], response["reason"])
                        df.at[index, 'Generated keywords'] = '[' + ', '.join(f'"{keyword}"' for keyword in keyword_suggestion_service.get_keywords([response['trend']])) + ']'
                    else:
                        df.at[index, 'Generated headlines'] = ''
                        df.at[index, 'Generated descriptions'] = ''
                        df.at[index, 'Generated keywords'] = ''

                    df.at[index, 'Ad Group ID'] = ''
                    df.at[index, 'Selection'] = 'FALSE'
                else:
                    df.at[index, 'relationship'] = 'UNDEFINED'

                if self.config["low_performance_mode"]:
                    time.sleep(0.5)

                bar()

            logging.info(f'Clearing google trends sheet')
            sheet_helper.clear_sheet(
                sheet_id = self.config['google_trends']['google_sheets']['spreadsheet_id'],
                sheet_name = self.config['google_trends']['google_sheets']['sheet_name'],
                sheet_range = "!A2:Z"
            )

            bar()

            logging.info(f'Writing data to sheet')
            sheet_helper.write_dataframe_to_gui(
                df,
                sheet_id = self.config["google_trends"]["google_sheets"]["spreadsheet_id"],
                sheet_name = self.config["google_trends"]["google_sheets"]["sheet_name"]
            )

            bar()

        logging.info(f'Finished')

        try:
            return jsonify({"message": "Google trends finished succesfully!"}), 200
        except:
            pass


    def __generate_headlines(self, trend, brand, reason) -> list:
        """
        Generates a list of headlines based on the trend, brand and association reason.

        Parameters:
        - trend (str): The trending topic.
        - brand (str): The brand to generate ad for.
        - reason (str): The reason why the topic and the brand are related.

        Returns:
        - list: A list of generated headlines.
        """
        return self.__generate_content('headlines', trend, brand, reason)


    def __generate_descriptions(self, trend, brand, reason) -> list:
        """
        Generates a list of descriptions based on the trend, brand and association reason.

        Parameters:
        - trend (str): The trending topic.
        - brand (str): The brand to generate ad for.
        - reason (str): The reason why the topic and the brand are related.

        Returns:
        - list: A list of generated descriptions.
        """
        return self.__generate_content('descriptions', trend, brand, reason)


    def __generate_content(self, type:str, trend:str, brand:str, reason:str) -> list:
        """
        Generates a list of content items of the specified type based on the trend, brand and association reason.

        Parameters:
        - type (str): The type of content to generate ('headlines' or 'descriptions').
        - trend (str): The trending topic.
        - brand (str): The brand to generate ad for.
        - reason (str): The reason why the topic and the brand are related.

        Returns:
        - list: A list of generated copies.
        """
        if type == 'headlines':
            max_length = 30
        elif type == 'descriptions':
            max_length = 90
        else:
            logging.error("Tried generating something other than 'headlines' or 'descriptions'")
            raise Exception(f"Unsupported value: {type}. Supported values are 'headlines' and 'descriptions'")

        generated_copies_with_size_enforced = []

        prompt = self.__get_copy_generation_prompt(type, trend, brand, reason)

        logging.info(f"Generating {type} for trend {trend} and brand {brand}")
        generated_copies = self.__generate_copies(prompt)
        logging.info(f"{type.capitalize()} for trend {trend} and brand {brand} generated")
        logging.info(f"{type.capitalize()}: {generated_copies}")

        logging.info(f"Enforcing {type} sizes for trend {trend} and brand {brand}")

        for copy in generated_copies:
            if len(copy) > max_length:
                copy_with_size_enforced = Utils.enforce_text_size(self.config, copy, type)
                if copy_with_size_enforced not in generated_copies_with_size_enforced:
                    generated_copies_with_size_enforced.append(copy_with_size_enforced)
            else:
                if copy not in generated_copies_with_size_enforced:
                    generated_copies_with_size_enforced.append(copy)

        logging.info(f"{type.capitalize()} for trend {trend} and brand {brand} generated and size enforced")
        logging.info(f"{type.capitalize()} with size enforcement: {generated_copies_with_size_enforced}")

        return '[' + ', '.join(f'"{copy}"' for copy in generated_copies_with_size_enforced) + ']'


    def __generate_copies(self, prompt:str, retries:int=1) -> list:
        """
        Generates copies based on the provided prompt.

        Parameters:
        - prompt (str): The prompt or input text for generating copies.
        - retries (int, optional): The number of retry attempts for content generation (default is 1).

        Returns:
        - list: A list of generated content items.
        """
        vertex_helper = VertexAIHelper(self.config)
        for _ in range(retries):
            try:
                return vertex_helper.generate_text_list_with_palm(prompt)
            except Exception as e:
                # TODO: manage
                logging.error(f'ERROR: {e}')


    def __get_trend_association_prompt(self, trend: str, brand: str, location: str) -> str:
        """
        Generates a text prompt for brand-trend association.

        Parameters:
        - trend (str): The trending topic to associate with the brand.
        - brand (str): The brand to associate with the trending topic.
        - location (str): The location from the trending topic.

        Returns:
        - str: A text prompt for brand-trend association.
        """
        return prompts[self.config['language']]['GOOGLE_TRENDS']['FIND_RELATIONSHIP'].format(
            trend=trend,
            brand=brand,
            location=location
        )


    def __get_copy_generation_prompt(self, type:str, trend:str, brand:str, association_reason:str) -> str:
        """
        Generates a text prompt for content generation.

        Parameters:
        - type (str): The type of content to generate (e.g., 'headlines', 'descriptions').
        - trend (str): The trending topic for the content.
        - association_reason (str): The reason why the trend and company are related.
        - brand (str): The name of the brand associated with the content.

        Returns:
        - str: A text prompt for content generation.
        """
        if type == 'headlines':
            length = 30
            number_of_copies = self.config["google_trends"]["google_ads"]["num_headlines"]
        elif type == 'descriptions':
            length = 90
            number_of_copies = self.config["google_trends"]["google_ads"]["num_descriptions"]
        else:
            raise Exception(f"Unsupported value: {type}. Supported values are 'headlines' and 'descriptions'")

        return prompts[self.config['language']]['GOOGLE_TRENDS']['COPIES_GENERATION'].format(
            n=number_of_copies,
            length=length,
            trend=trend,
            brand=brand,
            company=self.config["advertiser"],
            association_reason=association_reason,
            examples=str(self.config['palm_examples'][type]),
        )
