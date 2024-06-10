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

"""Authentication helper module.

This module contains all the methods for
authenticating with Google APIs.
"""

from google.auth import default
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

API_SCOPES = [
    'https://www.googleapis.com/auth/adwords',
    'https://www.googleapis.com/auth/bigquery',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/cloud-platform'
    ]


class Authenticator:
  """This class creates credentials to authenticate with google APIs."""

  def __init__(self) -> None:
    pass

  def authenticate(self, config: dict[str, str]) -> object:
    """Authentication method.

    Args:
      config (dict[str, str]): A dictionary containing configuration parameters.

    Returns:
      object: The credentials object.
    """
    client_id = config.get('client_id')
    client_secret = config.get('client_secret')
    refresh_token = config.get('refresh_token')

    if not client_id or not client_secret or not refresh_token:
      creds, _ = default(scopes=API_SCOPES)
    else:
      creds = Credentials.from_authorized_user_info({
          'client_id': client_id,
          'client_secret': client_secret,
          'refresh_token': refresh_token,
          })

    creds.refresh(Request())
    return creds
