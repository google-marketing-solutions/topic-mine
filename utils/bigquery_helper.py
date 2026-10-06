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

"""BigQuery helper module.

This module contains all the methods for
working with BigQuery.
"""

import logging

from google.cloud import bigquery
from utils.authentication_helper import Authenticator
from utils.utils import Utils

# Logger config
logging.basicConfig()
logging.root.setLevel(logging.INFO)


class BigQueryHelper:
  """BigQuery helper to read data from BigQuery using the specified client."""

  def __init__(self, config: dict[str, str]):
    """Initialize a BigQueryHelper instance.

    Args:
      config (dict[str, str]): A dictionary containing configuration parameters.
    """
    authenticator = Authenticator()
    creds = authenticator.authenticate(config)

    self.bigquery_client = bigquery.Client(
      credentials=creds,
      project=config['project_id']
    )

  def read_bigquery_column(
      self,
      project_id: str,
      dataset_id: str,
      table_id: str,
      column_name: str,
      limit: int
      ) -> list[str]:
    """Reads a specific column from a BigQuery table.

    Args:
      project_id (str): The ID of the Google Cloud project.
      dataset_id (str): The ID of the dataset containing the table.
      table_id (str): The ID of the table to read from.
      column_name (str): The name of the column to read.
      limit (int): The maximum number of rows to read.

    Returns:
      list[str]: A list containing the values of the specified column.
    """
    if not Utils.is_valid_project_id(project_id):
      raise ValueError(f'Invalid project_id: {project_id}')
    if not Utils.is_valid_bigquery_identifier(dataset_id):
      raise ValueError(f'Invalid dataset_id: {dataset_id}')
    if not Utils.is_valid_bigquery_identifier(table_id, allow_hyphen=True):
      raise ValueError(f'Invalid table_id: {table_id}')
    if not Utils.is_valid_bigquery_identifier(column_name):
      raise ValueError(f'Invalid column_name: {column_name}')
    if not isinstance(limit, int) or limit < 1:
      raise ValueError(f'Invalid limit: {limit}. Must be positive integer.')

    query = (
        'SELECT ' + column_name +
        ' FROM `' + project_id + '.' + dataset_id + '.' + table_id +
        '` LIMIT ' + str(limit)
        )

    rows = self.bigquery_client.query(query).result()
    column_values = [row[column_name] for row in rows]

    return column_values

  def run_query(self, query: str):
    """Runs a BigQuery query.

    Args:
      query (str): The query to run.

    Returns:
      list: A list containing the results of the query.
    """
    rows = self.bigquery_client.query(query).result()
    results = [row for row in rows]

    return results
