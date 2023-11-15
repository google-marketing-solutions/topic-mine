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
from utils.bigquery_helper import BigQueryHelper
from utils.vertex_ai_helper import VertexAIHelper
from utils.sheet_helper import GoogleSheetsHelper
from utils.google_ads_helper import GoogleAdsHelper
from utils.utils import Utils
import pandas as pd
import logging
from flask import jsonify
from prompts.prompts import prompts
import time

# Logger config
logging.basicConfig()
logging.root.setLevel(logging.INFO)


class ClientTrendsService:
    """
    This class contains methods for generating copies related with client trending topics and brands matching actions.
    """

    def __init__(self, config:dict):
        authenticator = Authenticator()
        self.creds = authenticator.authenticate_with_client_credentials(
            client_id = config["client_id"],
            client_secret = config["client_secret"],
            refresh_token = config["refresh_token"],
        )
        self.config = config


    def start(self, start_date, end_date) -> tuple:
        """
        Entry point for this service. Starts the copy generation process associated with client trends.
        Generates headlines and descriptions.

        Parameters:
        - start_date (str): The starting date to get the client trends data.
        - end_date (str): The ending date to get the client trends data.

        Returns:
        - tuple: Tuple with success message and code
        """
        logging.info('Starting client trends content generation from ClientTrendsService.start method')

        bigquery_helper = BigQueryHelper(self.config)
        sheet_helper = GoogleSheetsHelper(self.config)
        google_ads_helper = GoogleAdsHelper(self.config)

        logging.info('Fetching start and end dates for trends')
        logging.info('Start and end dates for trends fetched')

        query = self.config["client_trends"]["queries"]["trends"]
        limit = self.config["client_trends"]["big_query"]["trends_limit"]

        logging.info('Fetching base dataframe from big query')
        df = bigquery_helper.get_client_trending_products_from_bq(
            start_date = start_date,
            end_date = end_date,
            q = query,
            limit = limit
        )
        logging.info('Base dataframe fetched')

        logging.info('Generating headlines')
        headlines = self.__generate_headlines(df)
        df['generated_headlines'] = headlines
        logging.info('Headlines generated')

        logging.info('Generating descriptions')
        descriptions = self.__generate_descriptions(df)
        df['generated_descriptions'] = descriptions
        logging.info('Descriptions generated')

        logging.info('Generating keywords')
        keywords = google_ads_helper.get_keywords_suggestions(df['title'] if 'title' in df.columns else df['search_term'])
        df['generated_keywords'] = keywords
        logging.info('Keywords generated')

        df["start_date"] = start_date
        df["end_date"] = end_date

        df["selected"] = ''
        df["campaign_id"] = ''
        df["adgroup_id"] = ''

        bigquery_helper.load_table_from_dataframe(
            dataset_name = self.config["client_trends"]["big_query"]["dataset"],
            table_name = self.config["client_trends"]["big_query"]["current_state_table"],
            dataframe = df
        )

        logging.info(f'Clearing client trends sheet')
        sheet_helper.clear_sheet(
            sheet_id = self.config['client_trends']['google_sheets']['spreadsheet_id'],
            sheet_name = self.config['client_trends']['google_sheets']['sheet_name'],
            sheet_range = "!A2:Z"
        )

        logging.info(f'Writing client trends sheet')
        sheet_helper.write_dataframe_to_gui(
             df,
             sheet_id = self.config["client_trends"]["google_sheets"]["spreadsheet_id"],
             sheet_name = self.config["client_trends"]["google_sheets"]["sheet_name"]
        )

        logging.info(f'Finished!')

        try:
            return jsonify({"message": "Client trends finished succesfully!"}), 200
        except:
            pass


    def __generate_headlines(self, df:pd.DataFrame) -> list:
        """
        Generates a list of headlines based on the input DataFrame with the client trends information.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing the client trends information.

        Returns:
        - list: A list of generated headlines.
        """
        return self.__generate_content(df, 'headlines')


    def __generate_descriptions(self, df:pd.DataFrame) -> list:
        """
        Generates a list of descriptions based on the input DataFrame with the client trends information.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing the client trends information.

        Returns:
        - list: A list of generated descriptions.
        """
        return self.__generate_content(df, 'descriptions')


    def __generate_content(self, df:pd.DataFrame, type:str) -> list:
        """
        Generates a list of content items of the specified type based on the input DataFrame with the client trends information.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing the client trends information.
        - type (str): The type of content to generate ('headlines' or 'descriptions').

        Returns:
        - list: A 2D-list of generated content items of the specified type for each dataframe row.
        """
        if type == 'headlines':
            max_length = 30
        elif type == 'descriptions':
            max_length = 90
        else:
            logging.error("Tried generating something other than 'headlines' or 'descriptions'")
            raise Exception(f"Unsupported value: {type}. Supported values are 'headlines' and 'descriptions'")

        generated_copies_with_size_enforced = []

        for index, row in df.iterrows():
            generated_copies_with_size_enforced.append([])

            if type == 'headlines':
                max_length = 30
            elif type == 'descriptions':
                max_length = 90
            else:
                logging.error("Tried generating something other than 'headlines' or 'descriptions'")
                raise Exception(f"Unsupported value: {type}. Supported values are 'headlines' and 'descriptions'")

            prompt = self.__get_prompt(type, row['title'] if 'title' in df.columns else row['search_term'])

            logging.info(f"Generating {type} for product {row['title'] if 'title' in df.columns else row['search_term']}")
            generated_copies = self.__generate_copies(prompt)
            logging.info(f"{type.capitalize()} for product {row['title'] if 'title' in df.columns else row['search_term']} generated")
            logging.info(f"{type.capitalize()}: {generated_copies}")

            logging.info(f"Enforcing {type} sizes for product {row['title'] if 'title' in df.columns else row['search_term']}")

            for copy in generated_copies:
                if len(copy) > max_length:
                    copy_with_size_enforced = Utils.enforce_text_size(self.config, copy, type)
                    if copy_with_size_enforced not in generated_copies_with_size_enforced[index]:
                        generated_copies_with_size_enforced[index].append(copy_with_size_enforced)
                else:
                    if copy not in generated_copies_with_size_enforced[index]:
                        generated_copies_with_size_enforced[index].append(copy)

            logging.info(f"{type.capitalize()} for product {row['title'] if 'title' in df.columns else row['search_term']} generated and size enforced")
            logging.info(f"{type.capitalize()} with size enforcement: {generated_copies_with_size_enforced[index]}")

            if self.config["low_performance_mode"]:
                time.sleep(0.5)

        str_values = ['[' + ', '.join(f'"{copy}"' for copy in copies_per_product) + ']' for copies_per_product in generated_copies_with_size_enforced]

        return str_values


    def __get_prompt(self, type:str, title:str) -> str:
        """
        Generates a text prompt for content generation.

        Parameters:
        - type (str): The type of content to generate (e.g., 'headlines', 'descriptions').
        - title (str): The title or search term for the content.

        Returns:
        - str: A text prompt for content generation.
        """
        if type == 'headlines':
            length = 30
            number_of_copies = self.config["client_trends"]["google_ads"]["num_headlines"]
        elif type == 'descriptions':
            length = 90
            number_of_copies = self.config["client_trends"]["google_ads"]["num_descriptions"]
        else:
            raise Exception(f"Unsupported value: {type}. Supported values are 'headlines' and 'descriptions'")

        return prompts[self.config['language']]['CLIENT_TRENDS']['COPIES_GENERATION'].format(
            n=number_of_copies,
            length=length,
            title=title,
            company=self.config["advertiser"],
            examples=str(self.config['palm_examples'][type]),
        )


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
