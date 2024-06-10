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

import logging
import backoff

import gspread
from utils.authentication_helper import Authenticator


class GoogleSheetsHelper():
  """Helper class for working with Google Sheets using the Google Sheets API.
  """

  def __init__(self, config: dict[str, str]) -> None:
    """Initialize the GoogleSheetsHelper.

    Args:
      config (dict[str, str]): A dictionary containing configuration parameters.
    """
    authenticator = Authenticator()
    self.creds = authenticator.authenticate(config)
    self.client = gspread.authorize(self.creds)

  @backoff.on_exception(backoff.expo, gspread.exceptions.GSpreadException, max_tries=5)
  def create_or_clear_sheet(self, sheet_id: str, sheet_name: str) -> None:
    """Clear sheet if exists or create it if not exists.

    Args:
      sheet_id (str): The unique identifier of the Google Sheets spreadsheet.
      sheet_name (str): The name of the sheet (tab) in the spreadsheet.
    """
    logging.info(' Create or clear sheet: %s', sheet_name)

    spreadsheet = self.client.open_by_key(sheet_id)
    try:
      worksheet = spreadsheet.worksheet(sheet_name)
      worksheet.clear()
      logging.info(' Sheet %s found and cleared', sheet_name)
    except gspread.exceptions.WorksheetNotFound as _:
      _ = spreadsheet.add_worksheet(title=sheet_name, rows=10000, cols=100)
      logging.info(' Sheet %s created', sheet_name)
    except gspread.exceptions.GSpreadException as e:
      logging.error(' Error creating or clearing sheet: %s', e)
      raise  # Re-raise the exception so backoff can handle it

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
    spreadsheet = self.client.open_by_key(sheet_id)
    worksheet = spreadsheet.worksheet(sheet_name)
    column_values = (worksheet.col_values(ord(column) - 64)
                     [starting_row - 1:limit+starting_row-1])
    return column_values

  @backoff.on_exception(backoff.expo, gspread.exceptions.GSpreadException, max_tries=5)
  def write_data_to_sheet(
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
    logging.info(' Writing data to sheet: %s', sheet_name)

    try:
      spreadsheet = self.client.open_by_key(sheet_id)
      worksheet = spreadsheet.worksheet(sheet_name)
      worksheet.update(sheet_range, data)

      logging.info(' Data written successfully')
    except gspread.exceptions.GSpreadException as e:
      logging.error(' Error writing data: %s', e)
      raise  # Re-raise the exception so backoff can handle it

  def get_cell_value(
      self,
      sheet_id: str,
      sheet_name: str,
      row: int,
      column: str
      ) -> object:
    """Retrieve the value of a specific cell in the Google Sheet.

    Args:
      sheet_id (str): The ID of the Google Sheet.
      sheet_name (str): The name of the sheet in the Google Sheet.
      row (int): The row number of the cell.
      column (str): The column letter of the cell.

    Returns:
      object: The value of the specified cell.
    """
    spreadsheet = self.client.open_by_key(sheet_id)
    worksheet = spreadsheet.worksheet(sheet_name)
    cell_value = worksheet.cell(row, ord(column) - 64).value
    return cell_value
