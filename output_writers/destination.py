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

"""Parent Destination class.

This class is responsible for providing structural inheritance for all
destination subclasses.

For example:
  - DV360FeedDestination
  - SA360FeedDestination
"""

from utils.entry import Entry
from output_writers.validations import ValidationRule


class Destination:
  """Common set of methods that must be implemented by all destinations."""

  def __init__(self):
    """Init method for DestinationProto."""

  def write_destination_output(self, entries: list[Entry]) -> None:
    """Writes the output in the specificed destination.

    Sub-classes must implement this method

    Args:
      entries(list[Entry]): a list of source entries
    """

  def get_validation_rules(self) -> dict[str, list[ValidationRule]]:
    """Returns the set of validation rules for a destination.

    Sub-classes must implement this method.

    Returns:
      dict[str, list[ValidationRule]]: a dictionary of validation rules.
    """
    return {}

  def validate(self, rows: list[any]) -> list[str]:
    """Validates rows in a destination.

    Args:
      rows(list[any]): a list of rows to validate.

    Returns:
      list[str]: list of validation errors if any.
    """
