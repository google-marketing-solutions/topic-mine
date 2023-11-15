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

import googleapiclient.discovery as discovery
import gspread
from utils.authentication_helper import Authenticator
import pandas as pd


API_NAME = 'sheets'
API_VERSION = 'v4'
API_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class GoogleSheetsHelper():
    """
    Helper class for working with Google Sheets using the Google Sheets API.
    """

    def __init__(self,config:dict):
        """
        Initialize the GoogleSheetsHelper with the provided configuration.

        Args:
            config (dict): A dictionary containing configuration settings.

        Initializes the Google Sheets service using the provided credentials and configuration.

        Raises:
            google.auth.exceptions.DefaultCredentialsError: If credentials cannot be loaded.
        """
        # credentials, project = google.auth.default(scopes=API_SCOPES)
        self.config = config
        authenticator = Authenticator()
        self.creds = authenticator.authenticate_with_client_credentials(
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            refresh_token=config["refresh_token"],
        )
        self.service = discovery.build(API_NAME, API_VERSION, credentials = self.creds)


    def clear_sheet(self, sheet_id:str, sheet_name: str, sheet_range: str) -> None:
        """
        Clear data from a specific range in a Google Sheets spreadsheet.

        Args:
            sheet_id (str): The unique identifier of the Google Sheets spreadsheet.
            sheet_name (str): The name of the sheet (tab) in the spreadsheet.
            sheet_range (str): The range of cells to clear (e.g., "A1:B5").
        """
        request = self.service.spreadsheets().values().clear(
            spreadsheetId=sheet_id, range=f'{sheet_name}{sheet_range}')
        request.execute()


    def write_dataframe_to_gui(self, df: pd.DataFrame, sheet_id:str, sheet_name:str):
        """
        Writes the data from the provided DataFrame to the specified Google Sheets worksheet.

        Args:
            df (pd.DataFrame): The DataFrame to be written to the Google Sheets worksheet.
            sheet_id (str): The unique identifier of the Google Sheets spreadsheet.
            sheet_name (str): The name of the sheet (tab) in the spreadsheet.
        """
        # Call the Sheets API
        gc = gspread.authorize(self.creds)
        # Open the Google Spreadsheet by name and get the worksheet
        spreadsheet = gc.open_by_key(sheet_id)
        worksheet = spreadsheet.worksheet(sheet_name)
        # Write the DataFrame to the worksheet
        worksheet.clear()  # Clear the existing data
        worksheet.insert_rows([df.columns.tolist()], 1)  # Write DataFrame to worksheet, starting from the second row to keep headers
        worksheet.insert_rows(df.values.tolist(), 2)  # Write DataFrame to worksheet, starting from the second row to keep headers

