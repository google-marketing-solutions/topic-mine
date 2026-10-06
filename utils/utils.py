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

"""Utility functions for the application.
"""

import json
import re


class Utils:
  """This class contains multiple utilities.
  """

  @classmethod
  def load_config(cls, config_file_name: str) -> object:
    """Loads the configuration data from the given path.

    Args:
      config_file_name (str): The name of the configuration file to load.

    Returns:
      object: The contents of the configuration file as a JSON object.
    """
    config_file_path = './' + config_file_name
    with open(config_file_path, 'r') as config_file:
      return json.load(config_file)

  @classmethod
  def is_valid_bigquery_identifier(
      cls,
      identifier: object,
      allow_hyphen: bool = False,
      max_length: int = 1024
      ) -> bool:
    """Validates that a string is a safe BigQuery identifier (dataset, table, or column name).

    Args:
      identifier (object): The identifier to validate.
      allow_hyphen (bool): Whether to allow hyphens (permitted in some table IDs).
      max_length (int): Maximum allowable length.

    Returns:
      bool: True if valid, False otherwise.
    """
    if not isinstance(identifier, str) or not identifier:
      return False
    if len(identifier) > max_length:
      return False
    pattern = r'^[a-zA-Z0-9_\-]+$' if allow_hyphen else r'^[a-zA-Z0-9_]+$'
    return bool(re.match(pattern, identifier))

  @classmethod
  def is_valid_project_id(cls, project_id: object) -> bool:
    """Validates that a string is a safe GCP project ID.

    Args:
      project_id (object): The project ID to validate.

    Returns:
      bool: True if valid, False otherwise.
    """
    if not isinstance(project_id, str) or not project_id:
      return False
    if len(project_id) > 100 or len(project_id) < 1:
      return False
    return bool(re.match(r'^[a-zA-Z0-9_\-.:]+$', project_id))
