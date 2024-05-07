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

"""Module to perform generic evaluations on the data."""

import validators


class ValidationRule:
  """Class that defines a validation rule."""

  rule_description: str
  elements_to_validate: str
  error_message: str
  function: any

  def __init__(
      self,
      rule_description: str,
      elements_to_validate: str,
      error_message: str,
      function: any,
      ):
    self.rule_description = rule_description
    self.elements_to_validate = elements_to_validate
    self.error_message = error_message
    self.function = function


def is_number(value: str) -> bool:
  """Validate if value is numeric.

  Args:
    value(str): string representation of a number.

  Returns:
    bool: True if valid, False otherwise
  """
  return str(value).isnumeric()


def valid_url(url: str) -> bool:
  """Validate if url is valid.

  Args:
    url(str): the url to evaluate

  Returns:
    bool: True if valid, False otherwise
  """
  valid = validators.url(url)

  return isinstance(valid, bool)


def valid_length(item: str | list[any], min_limit: int, max_limit: int) -> bool:
  """Validate if item length (str or list) is within the limits.

  Args:
    item(str | list[any]): the item to evaluate, could be str or list
    min_limit(int): min allowed limit
    max_limit(int): max allowed limit

  Returns:
    bool: True if valid, False otherwise
  """
  return len(item) >= min_limit and len(item) <= max_limit


def unique_elements_in_list(list_check: list[any]) -> tuple[bool, list[any]]:
  """Validate if elements are unique in a list.

  Args:
    list_check(list[any]): the list to check for unique elements

  Returns:
    tuple[bool, list[any]]: True if valid, False otherwise and list of dups
  """
  seen = set()
  dupes = []
  for item in list_check:
    if item in seen:
      dupes.append(item)
    else:
      seen.add(item)
  return len(dupes) == 0, dupes


def are_all_words_upper_case(value: str) -> bool:
  """Validate if all words in a string are upper case.

  Args:
    value(str): the list to check for all upper case words

  Returns:
    bool: True if valid, False otherwise
  """
  return value.isupper()


def replace_single_quotes_with_double_quotes(value: str) -> str:
  """Replace single with double quotes.

  Args:
    value(str): value to replace the single quotes

  Returns:
    str: replaced string
  """
  return value.replace("'", '"')


def replace_square_brackets_with_curly_brackets(value: str) -> bool:
  """Replace square brackets with curly brackets.

  Args:
    value(str): value to replace the brackets

  Returns:
    str: replaced string
  """
  return value.replace("[", "{").replace("]", "}")
