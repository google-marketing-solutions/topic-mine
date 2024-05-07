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

from urllib import parse
from google_auth_oauthlib.flow import InstalledAppFlow
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError

flow = InstalledAppFlow.from_client_secrets_file(
    'creds.json',
    scopes=['https://www.googleapis.com/auth/adwords',
            'https://www.googleapis.com/auth/bigquery',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/cloud-platform'],
    )

flow.redirect_uri = 'http://localhost:8080'

auth_url, _ = flow.authorization_url(prompt='consent')

print(auth_url)

url = input('URL: ').strip()
code = parse.parse_qs(parse.urlparse(url).query)['code'][0]
try:
  flow.fetch_token(code=code)
except InvalidGrantError as ex:
  print('Authentication has failed: %s' % ex)


print('Access token: %s' % flow.credentials.token)
print('Refresh token: %s' % flow.credentials.refresh_token)
