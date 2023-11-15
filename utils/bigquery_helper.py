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

from google.cloud import bigquery
from typing import Any, List
from google.auth.transport.requests import Request
import pandas as pd
from google.cloud import exceptions as cloud_exceptions
from utils.authentication_helper import Authenticator




class BigQueryHelper:
    """BigQuery helper to read data from BigQuery using the specified client."""

    def __init__(self, config:dict):
        """
        Initialize a BigQueryHelper instance.

        Args:
            config (dict): A dictionary containing configuration parameters.
        """
        self.config = config
        self.project_id = config["project_id"]
        authenticator = Authenticator()
        self.creds = authenticator.authenticate_with_client_credentials(
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            refresh_token=config["refresh_token"],
        )
        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
        self.bigquery_client = bigquery.Client(credentials = self.creds, project = self.project_id)



    def execute_query(self, query: str) -> Any:
        """
        Execute a SQL query in BigQuery.

        Args:
            query (str): The SQL query to execute.

        Returns:
            Any: The result of the query execution.
        """
        query_job = self.bigquery_client.query(query)
        return query_job


    def create_dataset(self, dataset_name: str, location: str) -> None:
        """
        Create a new dataset in BigQuery.

        Args:
            dataset_name (str): The name of the dataset to create.
            location (str): The location where the dataset will be created.

        Returns:
            None
        """
        full_dataset_name = f"{self.project_id}.{dataset_name}"
        # Construct a full Dataset object to send to the API.
        dataset = bigquery.Dataset(full_dataset_name)
        dataset.location = location
        # Raises google.api_core.exceptions.Conflict if the Dataset already exists
        try:
            # Send the dataset to the API for creation, with an explicit timeout.
            dataset = self.bigquery_client.create_dataset(dataset, timeout=30)
            dataset_created = True if dataset and dataset.dataset_id else False
            if dataset_created:
                print(f"The dataset {full_dataset_name} was successfully created.")
        except cloud_exceptions.Conflict:
            print(f"The dataset {full_dataset_name} already exists.")


    def load_table_from_dataframe(self, dataset_name: str, table_name: str, dataframe: Any) -> None:
        """
        Load data from a DataFrame into a BigQuery table.

        Args:
            dataset_name (str): The dataset to save the table.
            table_name (str): The name of the table to create.
            dataframe (Any): The DataFrame containing the data to load.

        Returns:
            None
        """
        full_table_name = f"{self.project_id}.{dataset_name}.{table_name}"

        # Delete the existing table
        self.bigquery_client.delete_table(full_table_name, not_found_ok=True)  # Make an API request.
        print(f"Deleted table '{full_table_name}'")

        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
        # Make API request to load data
        job = self.bigquery_client.load_table_from_dataframe(
            dataframe, full_table_name, job_config=job_config
        )
        # Wait for the job to complete.
        job.result()
        # Check if table was created
        table = self.bigquery_client.get_table(full_table_name)
        if table:
            print(
                f"Loaded {table.num_rows} rows and {len(table.schema)} columns to table {full_table_name} successfully!"
            )
        else:
            print(
                f"There was an error loading the trends to the table {full_table_name}. The table could not be created."
            )


    def get_brands_from_merchant_center(self) -> List[Any]:
        """
        Retrieve a list of distinct brands from the Merchant Center table.

        Returns:
            List[Any]: A list of brand names.
        """
        query = "SELECT DISTINCT brand FROM `{0}`".format(
            self.config['google_trends']['brand_params']["merchant_center_table_name"]
        )
        # Make an API request.
        query_job = self.execute_query(query)
        brands = []
        for row in query_job:
            brands.append(row["brand"])
        return brands


    def google_trends_get_trends_from_bq(self, trends_params: Any) -> Any:
        """
        Retrieve google trends data from BigQuery.

        Args:
            trends_params (Any): Parameters for the trends query.

        Returns:
            Any: The retrieved trends data.
        """
        if trends_params["international"]:
            query = f"""
                SELECT
                    term,
                    ARRAY_AGG(STRUCT(term, rank, week, country_code, country_name, IF(score IS NULL, 0, score) AS score, refresh_date) ORDER BY week DESC LIMIT 1) AS trends
                FROM `bigquery-public-data.google_trends.international_top_terms`
                WHERE
                    week = (SELECT DATE_SUB(MAX(week), INTERVAL 52 week) FROM `bigquery-public-data.google_trends.international_top_terms`) # TODO @JGRIGGIO: Update the following line to see data for a given week. The week represents is the first day of the period the data represents
                    AND refresh_date = (SELECT MAX(refresh_date) FROM `bigquery-public-data.google_trends.international_top_terms`)
                    AND country_name = '{trends_params['country_name']}'
                GROUP BY 1
                ORDER BY (SELECT rank FROM UNNEST(trends))
            """
        else:
            query = """
                SELECT
                    term,
                    ARRAY_AGG(STRUCT(term, rank, week, dma_id, dma_name, IF(score IS NULL, 0, score) AS score, refresh_date) ORDER BY week DESC LIMIT 1) AS trends
                FROM `bigquery-public-data.google_trends.top_terms`
                WHERE
                    week = (SELECT DATE_SUB(MAX(week), INTERVAL 52 week) FROM `bigquery-public-data.google_trends.top_terms`) #Update the following line to see data for a given week. The week represents is the first day of the period the data represents
                    AND refresh_date = (SELECT MAX(refresh_date) FROM `bigquery-public-data.google_trends.top_terms`)
                GROUP BY 1
                ORDER BY (SELECT rank FROM UNNEST(trends));
            """ 
        # Make an API request.
        query_job = self.execute_query(query)
        top_terms = {}
        for row in query_job:
            # Row values can be accessed by field name or index.
            if row["term"] not in top_terms:
                top_terms[row["term"]] = row["trends"][0]
        return top_terms


    def get_client_trending_products_from_bq(
        self,
        start_date: str,
        end_date: str,
        q: str,
        limit: int,
        )-> pd.DataFrame:
        """
        Retrieve client trending products from BigQuery.

        Args:
            start_date (str): The start date for trend data in format YYYY-MM-DD.
            end_date (str): The end date for trend data in format YYYY-MM-DD.
            q (str): Query string for retrieving data.
            limit (int): The maximum number of elements in the final list.

        Returns:
            pd.DataFrame: A DataFrame containing the trending products.
        """
        query = q.format(start_date = start_date, end_date = end_date, limit = str(limit))
        df = self.bigquery_client.query(query).to_dataframe()
        return df
