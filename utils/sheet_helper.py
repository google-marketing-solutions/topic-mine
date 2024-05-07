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

"""Google Sheet Helper.

This module contains helper functions for working with Google Sheets.
"""

from googleapiclient import discovery
import gspread
from utils.authentication_helper import Authenticator

API_NAME = 'sheets'
API_VERSION = 'v4'
API_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class GoogleSheetsHelper():
  """Helper class for working with Google Sheets using the Google Sheets API.
  """

  def __init__(self, config: dict[str, str]) -> None:
    """Initialize the GoogleSheetsHelper with the provided configuration.

    Args:
      config (dict[str, str]): A dictionary containing configuration settings.

    Raises:
      google.auth.exceptions.DefaultCredentialsError: If credentials
      cannot be loaded.
    """
    self.config = config
    authenticator = Authenticator()
    self.creds = authenticator.authenticate_with_client_credentials(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        refresh_token=config['refresh_token']
        )
    self.service = discovery.build(
        API_NAME, API_VERSION,
        credentials=self.creds
        )

  def clear_sheet(
      self,
      sheet_id: str,
      sheet_name: str,
      sheet_range: str
      ) -> None:
    """Clear data from a specific range in a Google Sheets spreadsheet.

    Args:
      sheet_id (str): The unique identifier of the Google Sheets spreadsheet.
      sheet_name (str): The name of the sheet (tab) in the spreadsheet.
      sheet_range (str): The range of cells to clear (e.g., "A1:B5").
    """
    request = self.service.spreadsheets().values().clear(
        spreadsheetId=sheet_id, range=f'{sheet_name}!{sheet_range}')
    request.execute()

  def read_column_from_row(
      self,
      sheet_id: str,
      sheet_name: str,
      column: str,
      starting_row: int,
      limit: int
      ) -> list[object]:
    """Reads the data from the specified column starting from the given row in the provided Google Sheets worksheet.

    Args:
      sheet_id (str): The unique identifier of the Google Sheets spreadsheet.
      sheet_name (str): The name of the sheet (tab) in the spreadsheet.
      column (str): The column to be read.
      starting_row (int): The row number from which to start reading the values.
      limit (int): The maximum number of values to read.

    Returns:
      A list of values corresponding to the specified column starting
      from the given row.
    """
    # Call the Sheets API
    gc = gspread.authorize(self.creds)
    # Open the Google Spreadsheet by name and get the worksheet
    spreadsheet = gc.open_by_key(sheet_id)
    worksheet = spreadsheet.worksheet(sheet_name)
    # Get all values in the specified column starting from the given row
    column_values = worksheet.col_values(ord(column) - 64)[starting_row - 1:limit+starting_row-1]
    return column_values

  # def create_sheet_in_spreadsheet(self, sheet_name: str):
  #   """Creates a new sheet in the specified spreadsheet_id

  #   Args:
  #       sheet_name: the sheet name to read from
  #   Returns:
  #       sheet_id: the id of the new sheet created
  #   """
  #   try:
  #       sheet_id = self._find_sheet_id(sheet_name)
  #       # Create sheet in spreadsheet only if not previusly created
  #       if not sheet_id:
  #           request_body_create = self._build_create_sheet_request_body(sheet_name)
  #           request = self.service.spreadsheets().batchUpdate(
  #               spreadsheetId=self.spreadsheet_id, body=request_body_create
  #           )
  #           response = request.execute()
  #           # Get recently created sheet id
  #           sheet_id = self._find_sheet_id(sheet_name)
  #       return sheet_id
  #   except Exception as e:
  #       print(e)
  #       return None

  def write_data_to_sheet( # TODO TEST
      self,
      sheet_id: str,
      sheet_name: str,
      sheet_range: str,
      data: list[list[str]]
      ) -> None:
    """Write data to the specified Google Sheet.

    Args:
      sheet_id (str): The unique identifier of the Google Sheet.
      sheet_name (str): The name of the Google Sheet.
      sheet_range (str): The range to write data to, e.g., 'Sheet1!A1'.
      data (list[list[str]]): The data to be written.
    """
    # Create sheet if doesn't exist # TODO: FIX
    # sheet = self.create_sheet_in_spreadsheet(sheet_name)
    # if sheet:
    #   # Clear sheet first
    #   self.clear_sheet(sheet_name, sheet_range)

    body = {
        'values': data
    }
    self.service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=sheet_name + '!' + sheet_range,
        valueInputOption='RAW',
        body=body
    ).execute()

  def get_cell_value(
      self,
      sheet_id: str,
      sheet_name: str,
      row: int,
      column: str
      ) -> object:
    """
    Retrieve the value of a specific cell in the Google Sheet.

    Args:
      sheet_id (str): The ID of the Google Sheet.
      sheet_name (str): The name of the sheet in the Google Sheet.
      row (int): The row number of the cell.
      column (str): The column letter of the cell.

    Returns:
      object: The value of the specified cell.
    """
    gc = gspread.authorize(self.creds)
    spreadsheet = gc.open_by_key(sheet_id)
    worksheet = spreadsheet.worksheet(sheet_name)
    cell_value = worksheet.cell(row, ord(column) - 64).value
    return cell_value
