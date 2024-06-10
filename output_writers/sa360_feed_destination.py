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

"""SA360 Feed Destination class.

This class transforms and loads data to a Google sheet
with the correct format of an SA360 feed.
"""

import uuid
from output_writers import validations
from output_writers.destination import Destination
from output_writers.models.sa360_feed_row import SA360FeedRow
from output_writers.validations import ValidationRule
from utils.entry import Entry
from utils.sheet_helper import GoogleSheetsHelper

FEED_HEADERS = [
    'Id',
    'Publish',
    'Trend',
    'SKU',
    'Keywords',
    'Test URL',
    'Headline 1',
    'Headline 2',
    'Headline 3',
    'Headline 4',
    'Headline 5',
    'Headline 6',
    'Headline 7',
    'Headline 8',
    'Headline 9',
    'Headline 10',
    'Headline 11',
    'Headline 12',
    'Headline 13',
    'Headline 14',
    'Headline 15',
    'Description 1',
    'Description 2',
    'Description 3',
    'Description 4',
    'Campaign Id',
    'Ad Group Id',
]

VALIDATION_ERRORS_HEADERS = ['Error']

VALIDATION_LIMITS = {
    'headlines': {
        'min_len_limit': 3,
        'max_len_limit': 15,
        'min_char_len_limit': 5,  # check
        'max_char_len_limit': 30,
    },
    'descriptions': {
        'min_len_limit': 3,
        'max_len_limit': 4,
        'min_char_len_limit': 5,  # check
        'max_char_len_limit': 90,
    },
}


class SA360FeedDestination(Destination):
  """SA360 Feed Destination class.

  It transforms and loads data to a Google sheet
  with the correct format of an SA360 feed.
  """
  config: dict[str, str]
  sheets_helper: GoogleSheetsHelper

  def __init__(self, config: dict[str, str]):
    """Init method for SA360FeedDestination."""
    self.sheets_helper = GoogleSheetsHelper(config)
    self.config = config

  def write_destination_output(
      self,
      entries: list[Entry],
      sheet_id: str,
      sheet_name: str
      ) -> None:
    """Write output in SA360 format.

    Args:
      entries(list[Entry]): a list of source entries.
      sheet_id(str): the output sheet id.
      sheet_name(str): the output sheet name.
    """
    sa360_feed: list[list[str]] = [FEED_HEADERS]
    feed_rows = self._convert_entries_to_sa360_feed_rows(entries)
    # Perform validations for feed
    sa360_feed_errors: list[list[str]] = [VALIDATION_ERRORS_HEADERS]
    validation_errors = self.validate(feed_rows)
    # If there are validation errors, create a new sheet and load the errors
    if validation_errors:
      self.sheets_helper.create_or_clear_sheet(sheet_id, sheet_name + '_errors')

      for validation_error in validation_errors:
        sa360_feed_errors.append([validation_error])
      self.sheets_helper.write_data_to_sheet(
          sheet_id,
          sheet_name + '_errors',
          'A1:ZZ9999',
          sa360_feed_errors,
          )

    # Write feed_rows to the sheet
    for feed_row in feed_rows:
      self._append_columns_to_feed_row(feed_row, sa360_feed)

    self.sheets_helper.create_or_clear_sheet(sheet_id, sheet_name)

    self.sheets_helper.write_data_to_sheet(
        sheet_id,
        sheet_name,
        'A1:ZZ9999',
        sa360_feed
        )

  def get_validation_rules(self) -> dict[str, list[ValidationRule]]:
    """Returns the set of validation rules for an SA360 feed.

    Returns:
      dict[str, list[ValidationRule]]: a dictionary with the validation rules
    """
    validation_rules = {
      # TODO: REMOVE
        # 'all_rows_rules': [
        #     ValidationRule(
        #         'Validate unique skus',
        #         'skus',
        #         'Duplicate {elements} found: {duplicate_elements}.',
        #         self._validate_unique_skus,
        #     )
        # ],
        'single_row_rules': [
            # TODO: REMOVE
            # ValidationRule(
            #     'Validate Campaign Id is number',
            #     'campaign_id',
            #     'Id {row_id} - Campaign Id {campaign_id} should be a number.',
            #     self._validate_campaign_id,
            # ),
            # ValidationRule(
            #     'Validate Ad Group Id is number',
            #     'ad_group_id',
            #     'Id {row_id} - Ad Group Id {ad_group_id} should be a number.',
            #     self._validate_ad_group_id,
            # ),
            ValidationRule(
                'Validate URL is valid',
                'url',
                'Id {row_id} - The URL {url} should be a valid URL.',
                self._validate_url,
            ),
            ValidationRule(
                'Replace single quotes and square brackets in headline',
                'headlines',
                'Id {row_id} - Single quotes and square brackets replaced in {elements}',
                self._replace_single_quotes_square_brackets_in_element,
            ),
            ValidationRule(
                'Validate headlines list length',
                'headlines',
                'Id {row_id} - {elements} list should have min {min_len_limit} and max {max_len_limit} elements.',
                self._validate_elements_list_length,
            ),
            ValidationRule(
                'Validate headline character length',
                'headlines',
                'Id {row_id} - The following {elements}: {incorrect_char_len_elements} should have min {min_char_len_limit} and max {max_char_len_limit} characters.',
                self._validate_elements_char_length,
            ),
            # TODO: REMOVE
            # ValidationRule(
            #     'Validate unique headlines in list',
            #     'headlines',
            #     'Id {row_id} - Duplicate {elements} found: {duplicate_elements}.',
            #     self._validate_unique_elements_in_list,
            # ),
            ValidationRule(
                'Validate headline case',
                'headlines',
                'Id {row_id} - The following {elements}: {incorrect_case_elements} contain all words in uppercase.',
                self._validate_element_case,
            ),
            ValidationRule(
                'Replace single quotes and square brackets in description',
                'descriptions',
                'Id {row_id} - Single quotes and square brackets replaced in {elements}',
                self._replace_single_quotes_square_brackets_in_element,
            ),
            ValidationRule(
                'Validate descriptions list length',
                'descriptions',
                'Id {row_id} - {elements} list should have min {min_len_limit} and max {max_len_limit} elements.',
                self._validate_elements_list_length,
            ),
            ValidationRule(
                'Validate description character length',
                'descriptions',
                'Id {row_id} - The following {elements}: {incorrect_char_len_elements} should have min {min_char_len_limit} and max {max_char_len_limit} characters.',
                self._validate_elements_char_length,
            ),
            ValidationRule(
                'Validate unique descriptions in list',
                'descriptions',
                'Id {row_id} - Duplicate {elements} found: {duplicate_elements}.',
                self._validate_unique_elements_in_list,
            ),
            ValidationRule(
                'Validate description case',
                'descriptions',
                'Id {row_id} - The following {elements}: {incorrect_case_elements} contain all words in uppercase.',
                self._validate_element_case,
            ),
        ],
    }
    return validation_rules

  def validate(self, rows: list[SA360FeedRow]) -> list[str]:
    """Validate an SA360 feed.

    Args:
      rows(list[SA360FeedRow]): a list of SA360 feed rows to validate

    Returns:
      list[str]: list of validation errors if any
    """
    validation_rules = self.get_validation_rules()
    validation_errors = []
    # First: validate rules that require all rows in feed to perform validation
    validation_errors.extend(
        self.validate_rules(
            rows, validation_rules.get('all_rows_rules'), 'all_rows'
            )
        )

    for feed_row in rows:
      # Second: validate rules that apply to different columns in a single row
      validation_errors.extend(
          self.validate_rules(
              [feed_row],
              validation_rules.get('single_row_rules'),
              'single_row',
              )
          )
    return validation_errors

  def validate_rules(
      self,
      feed_rows: list[SA360FeedRow],
      validation_rules: list[ValidationRule],
      validation: str,
      ) -> list[str]:
    """Validate SA360 feed rows.

    Args:
      feed_rows(list[SA360FeedRow]): a list of feed rows to validate.
      validation_rules(list[ValidationRule]): a list of rules to validate rows.
      validation(str): 'all_rows' or 'single_row'.

    Returns:
      list[str]: list of validation errors if any.
    """
    validation_errors = []

    if not validation_rules:
      validation_rules = []

    for validation_rule in validation_rules:
      print(validation_rule.rule_description)
      if validation == 'all_rows':
        # validation_rule requires all rows to perform validation
        validation_message = validation_rule.function(
            feed_rows, validation_rule
            )
      else:
        # validation_rule requires single row to perform validation
        validation_message = validation_rule.function(
            feed_rows[0], validation_rule
            )
      if validation_message:
        validation_errors.append(validation_message)
    return validation_errors

  def _validate_unique_skus(
      self,
      feed_rows: list[SA360FeedRow],
      rule: ValidationRule
      ) -> str:
    """Validates if skus are unique in the feed.

    Args:
      feed_rows(list[SA360FeedRow]): list of feed rows to validate
      rule(ValidationRule): the rule  to validate feed rows

    Returns:
      str: an error message if rule not valid, empty otherwise
    """
    skus = set()
    duplicate_elements = []

    for feed_row in feed_rows:
      if feed_row.sku in skus:
        duplicate_elements.append(feed_row.sku)
      else:
        skus.add(feed_row.sku)

    if duplicate_elements:
      error_message = rule.error_message.replace(
          '{elements}', rule.elements_to_validate
          ).replace('{duplicate_elements}', ', '.join(duplicate_elements))
      return error_message

    return ''

  def _validate_campaign_id(
      self, feed_row: SA360FeedRow, rule: ValidationRule
      ) -> str:
    """Validates if Campaign Id is a number.

    Args:
      feed_row(SA360FeedRow): the current SA360 feed row to validate
      rule(ValidationRule): the rule to validate

    Returns:
      error_message: an error message if rule not valid, empty otherwise
    """
    valid = validations.is_number(feed_row.campaign_id)

    if not valid:
      error_message = rule.error_message.replace(
          '{row_id}', feed_row.row_id
          ).replace('{campaign_id}', str(feed_row.campaign_id))
      return error_message

    return ''

  def _validate_ad_group_id(
      self, feed_row: SA360FeedRow, rule: ValidationRule
      ) -> str:
    """Validates if Ad Group Id is a number.

    Args:
      feed_row(SA360FeedRow): the current SA360 feed row to validate
      rule(ValidationRule): the rule to validate

    Returns:
      str: an error message if rule not valid, empty otherwise
    """
    valid = validations.is_number(feed_row.ad_group_id)

    if not valid:
      error_message = rule.error_message.replace(
          '{row_id}', feed_row.row_id
          ).replace('{ad_group_id}', str(feed_row.ad_group_id))
      return error_message

    return ''

  def _validate_url(self, feed_row: SA360FeedRow, rule: ValidationRule) -> str:
    """Validates if url is valid.

    Args:
      feed_row(SA360FeedRow): the current SA360 feed row to validate
      rule(ValidationRule): the rule to validate

    Returns:
      str: an error message if rule not valid, empty otherwise
    """
    if feed_row.url and feed_row.url != '':
      valid = validations.valid_url(feed_row.url)

      if not valid:
        error_message = rule.error_message.replace(
            '{row_id}', feed_row.row_id
            ).replace('{url}', feed_row.url)
        return error_message

    return ''

  def _validate_elements_list_length(
      self, feed_row: SA360FeedRow, rule: ValidationRule
  ) -> str:
    """Validates if headlines/descriptions list length is within the limits.

    Args:
      feed_row(SA360FeedRow): the current SA360 feed row to validate
      rule(ValidationRule): the rule to validate

    Returns:
      str: an error message if rule not valid, empty otherwise
    """
    elements = getattr(feed_row, rule.elements_to_validate)
    valid = validations.valid_length(
        elements,
        VALIDATION_LIMITS.get(rule.elements_to_validate).get('min_len_limit'),
        VALIDATION_LIMITS.get(rule.elements_to_validate).get('max_len_limit'),
        )

    if not valid:
      error_message = (
          rule.error_message.replace('{row_id}', feed_row.row_id)
          .replace('{elements}', rule.elements_to_validate)
          .replace(
              '{min_len_limit}',
              str(
                  VALIDATION_LIMITS.get(rule.elements_to_validate).get(
                      'min_len_limit'
                  )
              ),
          )
          .replace(
              '{max_len_limit}',
              str(
                  VALIDATION_LIMITS.get(rule.elements_to_validate).get(
                      'max_len_limit'
                  )
              ),
          )
      )
      return error_message

    return ''

  def _validate_elements_char_length(
      self, feed_row: SA360FeedRow, rule: ValidationRule
  ) -> str:
    """Validates if headlines/descriptions char length is within the limits.

    Args:
      feed_row(SA360FeedRow): the current SA360 feed row to validate
      rule(ValidationRule): the rule to validate

    Returns:
        str: an error message if rule not valid, empty otherwise
    """
    elements = getattr(feed_row, rule.elements_to_validate)
    incorrect_char_len_elements = []
    for element in elements:
      if not validations.valid_length(
          element,
          VALIDATION_LIMITS.get(rule.elements_to_validate).get(
              'min_char_len_limit'
          ),
          VALIDATION_LIMITS.get(rule.elements_to_validate).get(
              'max_char_len_limit'
          ),
      ):
        incorrect_char_len_elements.append(element)

    if incorrect_char_len_elements:
      error_message = (
          rule.error_message.replace('{row_id}', feed_row.row_id)
          .replace('{elements}', rule.elements_to_validate)
          .replace(
              '{incorrect_char_len_elements}',
              ', '.join(incorrect_char_len_elements),
          )
          .replace(
              '{min_char_len_limit}',
              str(
                  VALIDATION_LIMITS.get(rule.elements_to_validate).get(
                      'min_char_len_limit'
                  )
              ),
          )
          .replace(
              '{max_char_len_limit}',
              str(
                  VALIDATION_LIMITS.get(rule.elements_to_validate).get(
                      'max_char_len_limit'
                  )
              ),
          )
      )
      return error_message

    return ''

  def _validate_unique_elements_in_list(
      self, feed_row: SA360FeedRow, rule: ValidationRule
  ) -> str:
    """Validates if headlines/descriptions in list are unique.

    Args:
      feed_row(SA360FeedRow): the current SA360 feed row to validate
      rule(ValidationRule): the rule to validate
    Returns:
      str: an error message if rule not valid, empty otherwise
    """
    elements = getattr(feed_row, rule.elements_to_validate)
    valid, duplicate_elements = validations.unique_elements_in_list(elements)

    if not valid:
      error_message = (
          rule.error_message.replace('{row_id}', feed_row.row_id)
          .replace('{elements}', rule.elements_to_validate)
          .replace('{duplicate_elements}', ','.join(duplicate_elements))
      )
      return error_message

    return ''

  def _validate_element_case(
      self, feed_row: SA360FeedRow, rule: ValidationRule
  ) -> str:
    """Validates if headlines/descriptions have a correct case.

    Args:
      feed_row(SA360FeedRow): the current SA360 feed row to validate
      rule(ValidationRule): the rule to validate
    Returns:
      str: an error message if rule not valid, empty otherwise
    """
    elements = getattr(feed_row, rule.elements_to_validate)
    incorrect_case_elements = []

    for element in elements:
      if validations.are_all_words_upper_case(element):
        incorrect_case_elements.append(element)

    if incorrect_case_elements:
      error_message = (
          rule.error_message.replace('{row_id}', feed_row.row_id)
          .replace('{elements}', rule.elements_to_validate)
          .replace(
              '{incorrect_case_elements}', ', '.join(incorrect_case_elements)
          )
      )
      return error_message

    return ''

  def _replace_single_quotes_square_brackets_in_element(
      self, feed_row: SA360FeedRow, rule: ValidationRule
  ) -> None:
    """Replaces single quotes and square brackets in headlines/descriptions.

    Args:
      feed_row(SA360FeedRow): the current SA360 feed row to validate
      rule(ValidationRule): the rule to validate
    """
    elements = getattr(feed_row, rule.elements_to_validate)

    for i, element in enumerate(elements):
      element = validations.replace_single_quotes_with_double_quotes(element)
      element = validations.replace_square_brackets_with_curly_brackets(element)
      elements[i] = element

  def _convert_entries_to_sa360_feed_rows(
      self, entries: list[Entry]
  ) -> list[SA360FeedRow]:
    """Converts a source entry to an SA360FeedRow for SA360 feed format.

    Args:
      entries(list[Entry]): a list of source entries.

    Returns:
      list[SA360FeedRow]: a list of source entry converted to an SA360FeedRow.
    """
    feed_rows = []

    for entry in entries:
      feed_rows.append(
          SA360FeedRow(
              row_id=str(uuid.uuid4()),
              publish='',
              trend=entry.term if entry.term else '',
              sku=entry.sku if entry.sku else '',
              keywords=entry.keywords if entry.keywords else [],
              url=entry.url if entry.url else '',
              headlines=entry.headlines if entry.headlines else [],
              descriptions=entry.descriptions if entry.descriptions else [],
              paths=[],
              campaign_id='',
              ad_group_id='',
          )
      )

    return feed_rows

  def _append_columns_to_feed_row(
      self, feed_row: SA360FeedRow, feed: list[list[str]]
  ) -> None:
    """Appends columns to each row and the row to the feed.

    Args:
      feed_row(SA360FeedRow): the current SA360 feed row
      feed(list[list[str]): a list of base columns for the feed
    """
    for keyword in feed_row.keywords:
      row_list = [
          feed_row.row_id,
          feed_row.publish,
          feed_row.trend,
          feed_row.sku,
          keyword,
          feed_row.url,
      ]
      for i in range(1, 15):
        if i <= len(feed_row.headlines):
          row_list.append(feed_row.headlines[i-1])
        else:
          row_list.append('')
      for i in range(1, 15):
        if i <= len(feed_row.descriptions):
          row_list.append(feed_row.descriptions[i-1])
        else:
          row_list.append('')
      for path in feed_row.paths:
        row_list.append(path)
      row_list.append(feed_row.campaign_id)
      row_list.append(feed_row.ad_group_id)
      feed.append(row_list)
