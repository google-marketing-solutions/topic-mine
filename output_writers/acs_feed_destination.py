# Copyright 2024 Google LLC
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

"""ACS Feed Destination class.

It transforms and loads data to a Google sheet
with the correct format of an ACS feed.
"""

from utils.entry import Entry
from utils.sheet_helper import GoogleSheetsHelper


class ACSFeedDestination:
  """ACS Feed Destination class.

  It transforms and loads data to a Google sheet
  with the correct format of an ACS feed.
  """

  config: dict[str, str]
  sheets_helper: GoogleSheetsHelper

  def __init__(self, config: dict[str, str]):
    """Init method for ACSFeedDestination."""
    self.sheets_helper = GoogleSheetsHelper(config)
    self.config = config

  def write_destination_output(
      self,
      entries: list[Entry],
      sheet_id: str,
      sheet_name: str,
      variant_name_column: str,
      constant_columns: list[str],
      copies_columns: list[str],
      starting_row: int
      ) -> None:
    """Write output in ACS format.

    Args:
      entries(list[Entry]): A list of source entries.
      sheet_id(str): The output sheet id.
      sheet_name(str): The output sheet name.
      variant_name_column(str): The column corresponding to the variant name.
      constant_columns(list[str]): Columns with constant values.
      copies_columns(list[str]): Columns to write generated content to.
      starting_row(int): Row to start writing content from.
    """
    acs_feed = self.__generate_feed(entries)

    self.sheets_helper.clear_sheet(
        sheet_id,
        sheet_name,
        f'A{starting_row + 1}:Z9999'
        )

    self.sheets_helper.write_data_to_sheet(
        sheet_id,
        sheet_name,
        f'{copies_columns[0]}{starting_row}:{copies_columns[-1]}9999',
        acs_feed
        )

    for column in constant_columns:
      value = self.sheets_helper.get_cell_value(
          sheet_id,
          sheet_name,
          starting_row,
          column
          )
      self.sheets_helper.write_data_to_sheet(
          sheet_id,
          sheet_name,
          f'{column}{starting_row}:{column}9999',
          [[value]] * len(entries)
          )

    variant_names = []
    for entry in entries:
      variant_names.append([' '.join(entry.headlines)]) # TODO: REVIEW

    self.sheets_helper.write_data_to_sheet(
        sheet_id,
        sheet_name,
        f'{variant_name_column}{starting_row}:{variant_name_column}9999',
        variant_names
        )

    if entries[0].associative_term:
      self.sheets_helper.write_data_to_sheet(
          sheet_id,
          sheet_name,
          # f'{second_term_column}{starting_row}:{second_term_column}9999',
          f'F{starting_row}:F9999',
          [[e.associative_term] for e in entries]
          )

  def __generate_feed(self, entries: list[Entry]) -> list[list[str]]:
    """Appends columns to each row and then the row to the feed.

    Args:
      entries(list[Entry]): The entries to generate feed

    Returns:
      list[list[str]]: the feed ready to be exported to spreadsheet
    """
    feed = []

    for entry in entries:
      row = []
      for h in entry.headlines:
        row.append(h)
      feed.append(row)

    return feed
