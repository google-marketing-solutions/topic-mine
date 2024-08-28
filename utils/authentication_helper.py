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
    self.client_id=None
    self.client_secret=None
    self.refresh_token=None
    self.is_authentication_method_client_id='unauthenticated'
    self.creds=None

  def has_been_authenticated_with_client_credentials(self):
    """
    Can return true if authenticated with client credentials
    Or false if it was done with service account
    else it will be a tring 'unauthenticated'
    """
    return self.is_authentication_method_client_id


  def authenticate(self, config: dict[str, str]) -> object:
    """Authentication method.

    Args:
      config (dict[str, str]): A dictionary containing configuration parameters.

    Returns:
      object: The credentials object.
    """
    self.client_id = config.get('client_id')
    self.client_secret = config.get('client_secret')
    self.refresh_token = config.get('refresh_token')

    if not self.client_id or not self.client_secret or not self.refresh_token:
      creds, _ = default(scopes=API_SCOPES)
      self.is_authentication_method_client_id=False
    else:
      creds = Credentials.from_authorized_user_info({
          'client_id': self.client_id,
          'client_secret': self.client_secret,
          'refresh_token': self.refresh_token,
          })
      self.is_authentication_method_client_id=True

    creds.refresh(Request())
    self.creds=creds
    return creds
