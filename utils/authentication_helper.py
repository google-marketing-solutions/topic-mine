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

from google.oauth2.credentials import Credentials


class Authenticator:
  """This class creates credentials to authenticate with google APIs."""

  def __init__(self) -> None:
    pass

  def authenticate_with_client_credentials(
      self,
      client_id: str,
      client_secret: str,
      refresh_token: str
      ) -> object:
    """Standard authentication for Google APIs.

    Args:
      client_id (str): The client_id.
      client_secret (str): The client_secret.
      refresh_token (str): The refresh_token.

    Returns:
      object: The credentials object.
    """

    creds = Credentials.from_authorized_user_info({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        })
    return creds
