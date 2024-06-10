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

"""DV360 Feed Destination class.

It transforms and loads data to a Google sheet
with the correct format of an DV360 feed.
"""

from utils.entry import Entry
from utils.sheet_helper import GoogleSheetsHelper


class DV360FeedDestination:
  """DV360 Feed Destination class.

  It transforms and loads data to a Google sheet
  with the correct format of an DV360 feed.
  """

  config: dict[str, str]
  sheets_helper: GoogleSheetsHelper

  def __init__(self, config: dict[str, str]):
    """Init method for DV360FeedDestination."""
    self.sheets_helper = GoogleSheetsHelper(config)
    self.config = config

  def write_destination_output(
      self,
      entries: list[Entry],
      sheet_id: str,
      sheet_name: str
      ) -> None:
    """Write output in DV360 format.

    Args:
      entries(list[Entry]): A list of source entries.
      sheet_id(str): the output sheet id.
      sheet_name(str): the output sheet name.
    """
    dv360_feed = self.__generate_feed(entries)

    self.sheets_helper.create_or_clear_sheet(sheet_id, sheet_name)

    self.sheets_helper.write_data_to_sheet(
        sheet_id,
        sheet_name,
        'A1:ZZ9999',
        dv360_feed
        )

  def __generate_feed(self, entries: list[Entry]) -> list[list[str]]:
    """Appends columns to each row and then the row to the feed.

    Args:
      entries(list[Entry]): The entries to generate feed

    Returns:
      list[list[str]]: the feed ready to be exported to spreadsheet
    """
    header = []
    header.append('Id')
    header.append('Term')
    if entries[0].term_description:
      header.append('Term Description')
    if entries[0].sku:
      header.append('SKU')
    if entries[0].associative_term:
      header.append('Associative Term')
    if entries[0].associative_term_description:
      header.append('Associative Term Description')
    if entries[0].url:
      header.append('URL')
    if entries[0].image_url:
      header.append('Image URL')
    if entries[0].association_reason:
      header.append('Association Reason')
    if entries[0].association_reason:
      header.append('Relationship')
    header.append('Headlines')
    header.append('Descriptions')
    header.append('Keywords')
    header.append('Active')
    header.append('Default')

    feed = []
    feed.append(header)

    for entry in entries:
      row = []
      row.append(str(entry.id))
      row.append(entry.term)
      if entry.term_description:
        row.append(entry.term_description)
      if entry.sku:
        row.append(entry.sku)
      if entry.associative_term:
        row.append(entry.associative_term)
      if entry.associative_term_description:
        row.append(entry.associative_term_description)
      if entry.url:
        row.append(entry.url)
      if entry.image_url:
        row.append(entry.image_url)
      if entry.association_reason:
        row.append(entry.association_reason)
      if entry.association_reason:
        row.append(entry.relationship)
      row.append('["{0}"]'.format('", "'.join(entry.headlines))
                 if entry.headlines else '')
      row.append('["{0}"]'.format('", "'.join(entry.descriptions))
                 if entry.descriptions else '')
      row.append('["{0}"]'.format('", "'.join(entry.keywords))
                 if entry.keywords else '')
      row.append('')
      row.append('')

      feed.append(row)

    return feed
