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

"""Content generator service.

This module contains all the methods for
associating two terms and generating content.
"""

import logging
import random
import re
import requests

from alive_progress import alive_bar
from prompts.prompts import prompts
from services.keyword_suggestion_service import KeywordSuggestionService
from utils.bigquery_helper import BigQueryHelper
from utils.entry import Entry
from utils.enums import FirstTermSource
from utils.enums import SecondTermSource
from utils.gemini_helper import GeminiHelper
from utils.sheet_helper import GoogleSheetsHelper

# Logger config
logging.basicConfig()
logging.root.setLevel(logging.INFO)


class ContentGeneratorService:
  """Methods for associating two terms and generating content.
  """
  entries: list[Entry]

  def __init__(self, config: dict[str, str]):
    self.config = config
    self.gemini_helper = GeminiHelper(self.config)
    self.bigquery_helper = BigQueryHelper(self.config)
    if 'google_ads_developer_token' in self.config and 'login_customer_id' in self.config:
        self.keyword_suggestion_service = KeywordSuggestionService(self.config)
    self.sheets_helper = GoogleSheetsHelper(self.config)

  def generate_content(
      self,
      first_term_source: FirstTermSource,
      second_term_source: SecondTermSource,
      must_find_relationship: bool,
      body_params: dict[str, str]
      ) -> list[Entry]:
    """Generates all the entries and content with AI.

    Args:
      first_term_source (FirstTermSource): The term's source .
      second_term_source (SecondTermSource): The second term's source.
      must_find_relationship (bool): If an association between
      first_term and second_term must be found.
      body_params (dict[str, str]): The body parameters of the request.

    Returns:
      list(Entry): A list of entries with content generated, ready to export.
    """
    logging.info(' Starting method generate_content')
    self.first_term_source = first_term_source
    self.second_term_source = second_term_source
    self.must_find_relationship = must_find_relationship
    self.body_params = body_params
    self.__generate_base_entries()
    with alive_bar(len(self.entries)) as self.bar:
      self.__populate_entries()
      return self.entries

  def __get_first_term_info_from_spreadsheet(
      self
      ) -> tuple[list[str], list[str], list[str], list[str], list[str]]:
    """Gets the terms, descriptions, skus, urls and image_urls from spreadsheet.

    Returns:
      tuple(list(str), list(str), list(str), list(str), list(str)):
      A tuple with a list of terms, descriptions, skus, urls and image_urls.
    """
    logging.info(' Getting terms and descriptions from spreadsheet')
    sheet_id = self.body_params['first_term_source_config']['spreadsheet_id']
    sheet_name = self.body_params['first_term_source_config']['sheet_name']
    starting_row = self.body_params['first_term_source_config']['starting_row']
    term_column = self.body_params['first_term_source_config']['term_column']
    limit = self.body_params['first_term_source_config']['limit']
    terms = self.sheets_helper.read_column_from_row(
        sheet_id,
        sheet_name,
        term_column,
        starting_row,
        limit
        )

    if ('term_description_column' in
        self.body_params['first_term_source_config']):
      term_description_column = (
          self.body_params['first_term_source_config']
          ['term_description_column']
          )
      descriptions = self.sheets_helper.read_column_from_row(
          sheet_id,
          sheet_name,
          term_description_column,
          starting_row,
          limit
          )
    else:
      descriptions = []

    if ('sku_column' in
        self.body_params['first_term_source_config']):
      sku_column = (
          self.body_params['first_term_source_config']
          ['sku_column']
          )
      skus = self.sheets_helper.read_column_from_row(
          sheet_id,
          sheet_name,
          sku_column,
          starting_row,
          limit
          )
    else:
      skus = []

    if 'url_column' in self.body_params['first_term_source_config']:
      url_column = self.body_params['first_term_source_config']['url_column']
      urls = self.sheets_helper.read_column_from_row(
          sheet_id,
          sheet_name,
          url_column,
          starting_row,
          limit
          )
    else:
      urls = []

    if 'image_url_column' in self.body_params['first_term_source_config']:
      image_url_column = (
          self.body_params['first_term_source_config']['image_url_column']
          )
      image_urls = self.sheets_helper.read_column_from_row(
          sheet_id,
          sheet_name,
          image_url_column,
          starting_row,
          limit
          )
    else:
      image_urls = []

    return terms, descriptions, skus, urls, image_urls

  def __get_first_term_info_from_bq(
      self
      ) -> tuple[list[str], list[str], list[str], list[str], list[str]]:
    """Gets the terms, descriptions, skus, urls and image_urls from bq.

    Returns:
      tuple(list(str), list(str), list(str), list(str), list(str)):
      A tuple with a list of terms, descriptions, skus, urls and image_urls.
    """
    logging.info(' Getting terms and descriptions from bq')
    if 'query' in self.body_params['first_term_source_config']:
      query = self.body_params['first_term_source_config']['query']
      r = self.bigquery_helper.run_query(query)
      terms = [row['term'] for row in r]
      descriptions = (
          [row['description'] for row in r]
          if 'description' in r[0].keys() else []
          )
      skus = [row['sku'] for row in r] if 'sku' in r[0].keys() else []
      urls = [row['url'] for row in r] if 'url' in r[0].keys() else []
      image_urls = (
          [row['image_url'] for row in r]
          if 'image_url' in r[0].keys() else []
          )

      return terms, descriptions, skus, urls, image_urls

    project_id = self.body_params['first_term_source_config']['project_id']
    dataset_id = self.body_params['first_term_source_config']['dataset']
    table_id = self.body_params['first_term_source_config']['table']
    term_column = self.body_params['first_term_source_config']['term_column']
    limit = self.body_params['first_term_source_config']['limit']
    terms = self.bigquery_helper.read_bigquery_column(
        project_id,
        dataset_id,
        table_id,
        term_column,
        limit
        )

    if ('term_description_column' in
        self.body_params['first_term_source_config']):
      term_description_column = (self.body_params
                                 ['first_term_source_config']
                                 ['term_description_column'])
      descriptions = self.bigquery_helper.read_bigquery_column(
          project_id,
          dataset_id,
          table_id,
          term_description_column,
          limit
          )
    else:
      descriptions = []

    if 'sku_column' in self.body_params['first_term_source_config']:
      sku_column = self.body_params['first_term_source_config']['sku_column']
      skus = self.bigquery_helper.read_bigquery_column(
          project_id,
          dataset_id,
          table_id,
          sku_column,
          limit
          )
    else:
      skus = []

    if 'url_column' in self.body_params['first_term_source_config']:
      url_column = self.body_params['first_term_source_config']['url_column']
      urls = self.bigquery_helper.read_bigquery_column(
          project_id,
          dataset_id,
          table_id,
          url_column,
          limit
          )
    else:
      urls = []

    if 'image_url_column' in self.body_params['first_term_source_config']:
      image_url_column = (
          self.body_params['first_term_source_config']
          ['image_url_column']
          )
      image_urls = self.bigquery_helper.read_bigquery_column(
          project_id,
          dataset_id,
          table_id,
          image_url_column,
          limit
          )
    else:
      image_urls = []

    return terms, descriptions, skus, urls, image_urls

  def __get_first_term_info(
      self
      ) -> tuple[list[str], list[str], list[str], list[str], list[str]]:
    """Gets the terms and descriptions to generate content for.

    Returns:
      tuple(list(str), list(str), list(str), list(str), list(str)):
      A tuple with a list of terms, descriptions, skus, urls and image_urls.
    """
    if self.first_term_source == FirstTermSource.SPREADSHEET:
      return self.__get_first_term_info_from_spreadsheet()
    elif self.first_term_source == FirstTermSource.BIG_QUERY:
      return self.__get_first_term_info_from_bq()
    else:
      raise ValueError(
          ('Invalid first-term-source query param. '
           'Supported values are spreadsheet and big_query.')
          )

  def __get_associative_terms_and_descriptions_from_gt(
      self
      ) -> tuple[list[str], list[str]]:
    """Gets the associative terms and descriptions from Google Trends.

    Returns:
      tuple(list(str), list(str)): A tuple with a list of
      associative terms and a list of associative terms descriptions.
    """
    logging.info(' Getting associative terms and descriptions from gt')
    query = f"""
            SELECT
                term, ARRAY_AGG(STRUCT(rank,week,country_name,country_code,score,refresh_date) ORDER BY week DESC LIMIT 1) x
            FROM
                `bigquery-public-data.google_trends.international_top_terms`
            WHERE
                refresh_date =
                    (SELECT
                        MAX(refresh_date)
                    FROM
                    `bigquery-public-data.google_trends.international_top_terms`
                    )
                AND country_name = '{self.config['country']}'
            GROUP BY
                term
            ORDER BY
                (SELECT rank FROM UNNEST(x))
            LIMIT {self.body_params['second_term_source_config']['limit']}
            """
    top_terms = {}

    result = self.bigquery_helper.run_query(query)
    for row in result:
      if row[0] not in top_terms:
        top_terms[row[0]] = row[1][0]

    return list(top_terms.keys()), []

  def __get_associative_terms_and_descriptions_from_ss(
      self
      ) -> tuple[list[str], list[str]]:
    """Gets the associative terms and descriptions from ss.

    Returns:
      tuple(list(str), list(str)): A tuple with a list of
      associative terms and a list of descriptions.
    """
    logging.info(' Getting associative terms and descriptions from ss')
    project_id = self.body_params['second_term_source_config']['project_id']
    dataset_id = self.body_params['second_term_source_config']['dataset']
    table_id = self.body_params['second_term_source_config']['table']
    term_column = self.body_params['second_term_source_config']['term_column']
    limit = self.body_params['second_term_source_config']['limit']
    terms = self.bigquery_helper.read_bigquery_column(
        project_id,
        dataset_id,
        table_id,
        term_column,
        limit
        )
    if ('term_description_column' in
        self.body_params['second_term_source_config']):
      term_description_column = (
          self.body_params['second_term_source_config']
          ['term_description_column']
          )
      descriptions = self.bigquery_helper.read_bigquery_column(
          project_id,
          dataset_id,
          table_id,
          term_description_column,
          limit
          )
    else:
      descriptions = []

    final_terms = []
    final_descriptions = []
    for term in terms:
      final_terms.append(term)
    for description in descriptions:
      final_descriptions.append(description)
    return final_terms, final_descriptions

  def __get_associative_terms_and_descriptions_from_rss(
      self
      ) -> tuple[list[str], list[str]]:  # TODO: implement
    """Gets the associative terms and descriptions from rss.

    Returns:
      tuple(list(str), list(str)): A tuple with a list of associative
      terms and a list of descriptions.
    """
    logging.info(' Getting associative terms and descriptions from rss')
    return [], []

  def __get_associative_terms_and_descriptions_from_spreadsheet(
      self
      ) -> tuple[list[str], list[str]]:
    """Gets the associative terms and descriptions from spreadsheet.

    Returns:
      tuple(list(str), list(str)): A tuple with a list of associative
      terms and a list of descriptions.
    """
    logging.info(' Getting associative terms and descriptions from spreadsheet')
    sheet_id = self.body_params['second_term_source_config']['spreadsheet_id']
    sheet_name = self.body_params['second_term_source_config']['sheet_name']
    starting_row = self.body_params['second_term_source_config']['starting_row']
    term_column = self.body_params['second_term_source_config']['term_column']
    limit = self.body_params['second_term_source_config']['limit']
    if ('term_description_column' in
        self.body_params['second_term_source_config']):
      term_description_column = (
          self.body_params['second_term_source_config']
          ['term_description_column']
          )
      descriptions = self.sheets_helper.read_column_from_row(
          sheet_id,
          sheet_name,
          term_description_column,
          starting_row,
          limit
          )
    else:
      descriptions = []

    associative_terms = self.sheets_helper.read_column_from_row(sheet_id,
                                                                sheet_name,
                                                                term_column,
                                                                starting_row,
                                                                limit
                                                                )
    return associative_terms, descriptions

  def __get_associative_terms_and_descriptions(
      self
      ) -> tuple[list[str], list[str]]:
    """Gets the associative terms and descriptions given the origin requested.

    Returns:
      tuple(list(str), list(str)): A tuple with a list of associative
      terms and a list of associative terms descriptions.
    """
    if self.second_term_source == SecondTermSource.NONE:
      return [], []
    if self.second_term_source == SecondTermSource.GOOGLE_TRENDS:
      return self.__get_associative_terms_and_descriptions_from_gt()
    elif self.second_term_source == SecondTermSource.SEARCH_SCOUT:
      return self.__get_associative_terms_and_descriptions_from_ss()
    elif self.second_term_source == SecondTermSource.RSS_FEED:
      return self.__get_associative_terms_and_descriptions_from_rss()
    elif self.second_term_source == SecondTermSource.SPREADSHEET:
      return self.__get_associative_terms_and_descriptions_from_spreadsheet()
    else:
      raise ValueError(
          ('Invalid second-term-source query param. Supported values are '
           'none, google_trends, search_scout, rss_feed and spreadsheet.')
          )

  def __remove_double_quotes(self, terms: list[str]) -> list[str]:
    """Removes the double quotes from the terms.

    Args:
      terms (list[str]): A list of terms.

    Returns:
      list[str]: A list of terms without the double quotes.
    """
    return [term.replace('"', '\'') for term in terms]

  def __check_and_replace_urls(self, urls):
    """
    Checks the validity and status code of a list of URLs. Replaces invalid
    or unreachable URLs with a generic URL, but considers redirects as valid.

    Args:
      urls (list[str]): A list of URLs to check.

    Returns:
      A new list of URLs with invalid/unreachable ones replaced.
    """

    valid_urls = []

    for url in urls:
      try:
        response = requests.head(url, allow_redirects=True, timeout=5)

        # 200 = OK, 301/302 = Redirect
        if response.status_code in (200, 301, 302):
          # Append the final URL after redirects
          valid_urls.append(response.url)
        else:
          if self.body_params['url_validation'] == 'REMOVE_BROKEN_URLS':
            valid_urls.append('')
          elif self.body_params['url_validation'] == 'USE_DEFAULT_URL':
            valid_urls.append(self.body_params['default_url'])

      except (requests.exceptions.RequestException,
              requests.exceptions.InvalidURL):
        if self.body_params['url_validation'] == 'REMOVE_BROKEN_URLS':
          valid_urls.append('')
        elif self.body_params['url_validation'] == 'USE_DEFAULT_URL':
          valid_urls.append(self.body_params['default_url'])

    return valid_urls

  def __generate_base_entries(self) -> None:
    """Generates the list of entries that will be then populated with generated content.
    """
    self.entries = []

    (terms, descriptions, skus,
     urls, image_urls) = self.__get_first_term_info()

    try:
      if (self.body_params['url_validation'] == 'REMOVE_BROKEN_URLS'
          or self.body_params['url_validation'] == 'USE_DEFAULT_URL'):
        urls = self.__check_and_replace_urls(urls)
    except KeyError as _:
      pass

    terms = self.__remove_double_quotes(terms)
    if descriptions:
      descriptions = self.__remove_double_quotes(descriptions)

    try:
      if self.body_params['enable_feature_extraction']:
        descriptions = self.__extract_main_features(descriptions)
    except KeyError as _:
      pass

    associative_terms, associative_terms_descriptions = (
        self.__get_associative_terms_and_descriptions()
        )

    associative_terms = self.__remove_double_quotes(associative_terms)
    if associative_terms_descriptions:
      associative_terms_descriptions = self.__remove_double_quotes(associative_terms_descriptions)

    if associative_terms:
      for i in range(0, len(terms)):
        for j in range(0, len(associative_terms)):
          entry = Entry(
              terms[i].capitalize(),
              descriptions[i].capitalize() if descriptions and descriptions[i] else None,
              associative_terms[j].capitalize(),
              (associative_terms_descriptions[j].capitalize()
               if associative_terms_descriptions and associative_terms_descriptions[j] else None),
              skus[i] if skus else None,
              urls[i] if urls else None,
              image_urls[i] if image_urls else None
              )
          self.entries.append(entry)
    else:
      for i in range(0, len(terms)):
        entry = Entry(
            terms[i].capitalize(),
            descriptions[i].capitalize() if descriptions and descriptions[i] else None,
            None,
            None,
            skus[i] if skus else None,
            urls[i] if urls else None,
            image_urls[i] if image_urls else None
            )
        self.entries.append(entry)

  def __populate_entries(self) -> None:
    """Populates each entry with headlines, descriptions and keywords.
    """
    i = 0
    while i < len(self.entries):
      if self.must_find_relationship:
        self.__find_association(self.entries[i])

      if self.entries[i].must_generate_content(self.must_find_relationship):
        self.__generate_content(self.entries[i])

      if self.entries[i].has_generation_errors() and not self.entries[i].has_been_cleared:
        self.entries.remove(self.entries[i])
        self.entries[i].clear_generated_content()
        self.entries.append(self.entries[i])
      else:
        self.bar()
        i = i + 1

  def __find_association(self, entry: Entry) -> None:
    """Tries to find a relationship between the term and the associative term for a given entry.

    Args:
      entry (Entry): The entry with both terms to try to associate.
    """
    logging.info(
        ' Getting association info between %s and %s',
        entry.term,
        entry.associative_term
        )
    prompt = self.__get_association_prompt(entry)
    response = self.gemini_helper.generate_dict(prompt)

    try:
      entry.association_reason = response['reason']
      entry.relationship = (
          response['relationship'] or response['relationship'] == 'true'
          )
      logging.info(
          ' Relationship: %s - %s',
          entry.relationship,
          entry.association_reason
          )
    except KeyError as _:
      entry.association_reason = 'No association found'
      entry.relationship = False
      logging.info(
          ' No relationship found because of bad Gemini generation: %s',
          {response}
          )

  def __generate_content(self, entry: Entry) -> None:
    """Generates the headlines, descriptions and keywords for a given entry.

    Args:
      entry (Entry): The entry to generate content for.
    """
    headlines = []
    descriptions = []
    keywords = []
    paths = []


    if self.body_params['num_headlines'] != 0:
      logging.info(' Generating headlines for term %s', entry.term)
      headlines = self.__generate_copies(
          entry,
          'headlines',
          self.body_params['num_headlines']
          )
      logging.info(' Headlines: %s', headlines)

    if self.body_params['num_descriptions'] != 0:
      logging.info(' Generating descriptions for term %s', entry.term)
      descriptions = self.__generate_copies(
          entry,
          'descriptions',
          self.body_params['num_descriptions']
          )
      logging.info(' Descriptions: %s', descriptions)

    logging.info(' Generating keywords for term %s', entry.term)
    keywords = self.__get_keywords([entry.term])
    logging.info(' Keywords: %s', keywords)

    if 'generate_paths' in self.body_params and self.body_params['generate_paths']:
      logging.info(' Generating paths for term %s', entry.term)
      paths = self.__generate_copies(entry, 'paths', 2)
      logging.info(' Paths: %s', paths)

    entry.headlines = headlines
    entry.descriptions = descriptions
    entry.keywords = keywords
    entry.paths = paths

  def __get_keywords(self, term: list[str]) -> list[str]:
    """Gets keywords for a given term.

    Args:
      term (list[str]): The term to get keywords for.
    Returns:
      list[str]: A list of keywords.
    """
    keywords = []
    if 'google_ads_developer_token' in self.config and 'login_customer_id' in self.config:
      keywords = self.keyword_suggestion_service.get_keywords(term)

    if not keywords:
      prompt = f"""
                Dado el término '{term}', dame una lista de hasta 10 keywords para Google ads que pueda usar relacionadas con el término.
                Dame el resultado de la siguiente forma:
                ["Característica 1", "Característica 2", ..., "Característica N"]
                La respuesta debes darmela exactamente en el formato que te he pasado, sin agregar saltos de linea ni espacios innecesarios. Solo debe ser una lista de keywords separados por comas, todo entre corchetes y nada mas.
                """
      keywords = self.gemini_helper.generate_text_list(prompt)

    return keywords

  def __check_blacklists(
      self,
      t: str,
      copies: list[str]
      ) -> list[str]:
    """Check copies and remove them if they contain blacklisted terms or regexes.

    Args:
      t (str): The type of copies (headlines|descriptions).
      copies (list[str]): A list of copies.

    Returns:
      list(str): A list of copies that are not blacklisted.
    """
    if t == 'headlines':
      try:
        for term in self.body_params['headlines_blacklist']:
          i = 0
          while i < len(copies):
            if term.lower() in copies[i].lower():
              copies.remove(copies[i])
            else:
              i = i + 1
      except KeyError as _:
        pass

      try:
        for regexp in self.body_params['headlines_regexp_blacklist']:
          pattern = re.compile(regexp)
          i = 0
          while i < len(copies):
            if pattern.match(copies[i]):
              copies.remove(copies[i])
            else:
              i = i + 1
      except KeyError as _:
        pass
    elif t == 'descriptions':
      try:
        for term in self.body_params['descriptions_blacklist']:
          i = 0
          while i < len(copies):
            if term.lower() in copies[i].lower():
              copies.remove(copies[i])
            else:
              i = i + 1
      except KeyError as _:
        pass

      try:
        for regexp in self.body_params['descriptions_regexp_blacklist']:
          pattern = re.compile(regexp)
          i = 0
          while i < len(copies):
            if pattern.match(copies[i]):
              copies.remove(copies[i])
            else:
              i = i + 1
      except KeyError as _:
        pass

    return copies

  def __fill_with_generic_copies(
      self,
      copies: list[str],
      t: str,
      num_copies: int
      ) -> list[str]:
    """Fill copy list with generic copies if available.

    Args:
      copies (list[str]): A list of copies.
      t (str): The type of copies (headlines|descriptions).
      num_copies (int): The total number of copies needed.

    Returns:
      list(str): A list of copies.
    """
    try:
      generic_copies_pool = self.body_params['generic_copies'][t]
    except KeyError as _:
      generic_copies_pool = []

    while generic_copies_pool and len(copies) < num_copies:
      random_copy = random.choice(generic_copies_pool)
      copies.append(random_copy)

    while len(copies) < num_copies:
      copies.append('Generation error')

    return copies

  def __generate_copies(
      self,
      entry: Entry,
      t: str,
      num_copies: int,
      retries_left: int = 2
      ) -> list[str]:
    """Generates a list of copies based on the entry and copy type.

    Args:
      entry (Entry): The entry to generate copies for.
      t (str): The type of copies (headlines|descriptions).
      num_copies (int): The number of copies to generate.
      retries_left (int): The number of retries if not enough copies
      are generated.

    Returns:
      list(str): A list of copies.
    """
    if num_copies == 0:
      return []

    if t == 'headlines':
      max_length = 30
    elif t == 'descriptions':
      max_length = 90
    elif t == 'paths':
      max_length = 15

    # Get copy generation prompt
    prompt = self.__get_copy_generation_prompt(t, entry, num_copies)

    # Generate copies
    generated_copies = self.gemini_helper.generate_text_list(
        prompt
        )

    generated_copies_with_size_enforced = []

    i = 0
    while i < len(generated_copies):
      # Remove errors
      if 'failed' in generated_copies[i].lower() or 'error' in generated_copies[i].lower():
        generated_copies.remove(generated_copies[i])
        continue

      # Remove extra whitespaces
      generated_copies[i] = generated_copies[i].strip()

      # Remove full stop if it is a headline
      try:
        generated_copies[i] = generated_copies[i][:-1] if generated_copies[i][-1] == '.' and t == 'headlines' else generated_copies[i]
      except IndexError as _:
        pass

      # Enforce size
      if len(generated_copies[i]) > max_length:
        copy_with_size_enforced = self.gemini_helper.enforce_text_size(
            generated_copies[i],
            t
            )

        # Remove full stop if it is a headline
        try:
          copy_with_size_enforced = (
              copy_with_size_enforced[:-1] if copy_with_size_enforced[-1]
              == '.' and t == 'headlines' else copy_with_size_enforced
              )
        except IndexError as _:
          pass
      else:
        copy_with_size_enforced = generated_copies[i]

      # Remove duplicates
      if copy_with_size_enforced not in generated_copies_with_size_enforced:
        generated_copies_with_size_enforced.append(copy_with_size_enforced)

      i = i + 1

    # Remove copies that are blacklisted
    generated_copies_with_size_enforced = self.__check_blacklists(
        t,
        generated_copies_with_size_enforced
        )

    # Remove copies that are 2 words or less
    for copy in generated_copies_with_size_enforced:
      copy_splitted = copy.split(' ')
      if len(copy_splitted) <= 2:
        generated_copies_with_size_enforced.remove(copy)

    # If retries still available and not enough copies, generate more
    if (
        len(generated_copies_with_size_enforced) < num_copies
        and retries_left > 0
        ):
      logging.info(
          ' Not enough copies generated. Generating more. Retries left: %d...',
          retries_left
          )
      return (
          generated_copies_with_size_enforced +
          self.__generate_copies(
              entry,
              t,
              num_copies - len(generated_copies_with_size_enforced),
              retries_left - 1)
          )

    # If no retries left and not enough copies, add generic copies
    if (
        len(generated_copies_with_size_enforced) < num_copies
        and retries_left == 0
        ):
      generated_copies_with_size_enforced = self.__fill_with_generic_copies(
          generated_copies_with_size_enforced,
          t,
          num_copies
          )

    return generated_copies_with_size_enforced

  def __extract_main_features(self, descriptions: list[str]) -> list[str]:
    """Extract main features from a given product description.

    Args:
      descriptions (list[str]): A list of product descriptions.

    Returns:
      list(str): A list of main features for each product description.
    """
    logging.info(' Extracting main features from descriptions...')
    with alive_bar(len(descriptions)) as feature_extraction_progress_bar:
      main_features_for_all_descriptions = []
      for description in descriptions:
        prompt = f"""
                Dada la siguiente descripcion de producto:
                "{description}"
                Dame una lista breve de las caracteristicas principales.
                Dame el resultado en el siguiente formato:
                "Característica 1", "Característica 2", ..., "Característica N"
              """
        try:
          main_features = self.gemini_helper.run_prompt(
              prompt
              )
          main_features_for_all_descriptions.append(main_features)
        except:
          main_features_for_all_descriptions.append(description)
        feature_extraction_progress_bar()
    return main_features_for_all_descriptions

  def __get_association_prompt(self, entry: Entry) -> str:
    """Generates a text prompt for term-associative_term association.

    Args:
      entry (Entry): The entry to retrieve the info to generate prompt.

    Returns:
      str: A text prompt for term-associative_term association.
    """
    if (
        entry.term_description is not None
        and entry.associative_term_description is not None
        ):
      first_part = (
          prompts[self.config['language']]
          ['ASSOCIATION']['WITH_BOTH_DESCRIPTIONS']
          ).format(
              term=entry.term,
              term_description=entry.term_description,
              associative_term=entry.associative_term,
              associative_term_description=entry.associative_term_description
              )
    elif (
        entry.term_description is not None
        and entry.associative_term_description is None
        ):
      first_part = (
          prompts[self.config['language']]['ASSOCIATION']
          ['WITH_TERM_DESCRIPTION']
          ).format(
              term=entry.term,
              term_description=entry.term_description,
              associative_term=entry.associative_term
              )
    elif (
        entry.term_description is None
        and entry.associative_term_description is not None
        ):
      first_part = (
          prompts[self.config['language']]['ASSOCIATION']
          ['WITH_ASSOCIATIVE_TERM_DESCRIPTION']
          ).format(
              term=entry.term,
              associative_term=entry.associative_term,
              associative_term_description=entry.associative_term_description
              )
    elif (
        entry.term_description is None
        and entry.associative_term_description is None
        ):
      first_part = (
          prompts[self.config['language']]['ASSOCIATION']
          ['WITHOUT_DESCRIPTIONS']
          ).format(
              term=entry.term,
              associative_term=entry.associative_term
              )

    second_part = (
        prompts[self.config['language']]['ASSOCIATION']
        ['COMMON_PART']
        ).format(
            term=entry.term,
            associative_term=entry.associative_term
            )

    return first_part + second_part

  def __get_copy_generation_prompt(
      self,
      t: str,
      entry: Entry,
      number_of_copies: int
      ) -> str:
    """Generates a text prompt for content generation.

    Args:
      t (str): The type of content to generate
      (e.g., 'headlines', 'descriptions').
      entry (Entry): The entry to retrieve the info to generate prompt.
      number_of_copies (int): number of copies to generate

    Returns:
      str: A text prompt for content generation.

    Raises:
      ValueError: If the type is not supported.
    """
    if t == 'headlines':
      length = 30
    elif t == 'descriptions':
      length = 90
    elif t == 'paths':
      length = 15
      if entry.term_description:
        return prompts[self.config['language']]['GENERATION']['PATHS_WITH_TERM_DESCRIPTION'].format(
                  n=number_of_copies,
                  length=length,
                  term=entry.term,
                  term_description=entry.term_description,
                  )
      else:
        return prompts[self.config['language']]['GENERATION']['PATHS_WITHOUT_TERM_DESCRIPTION'].format(
                  n=number_of_copies,
                  length=length,
                  term=entry.term,
                  )
    else:
      raise ValueError("Only types supported: 'headlines' and 'descriptions'")

    if entry.has_associative_term() and not self.must_find_relationship:
      return (
          prompts[self.config['language']]['GENERATION']
          ['WITH_ASSOCIATIVE_TERM']['WITHOUT_RELATIONSHIP_AND_DESCRIPTIONS']
          ).format(
              n=number_of_copies,
              length=length,
              term=entry.term,
              associative_term=entry.associative_term,
              )

    if not entry.has_associative_term():
      if not entry.term_description:
        return (
            prompts[self.config['language']]['GENERATION']
            ['WITHOUT_ASSOCIATIVE_TERM']['WITHOUT_DESCRIPTION']
            ).format(
                n=number_of_copies,
                length=length,
                term=entry.term,
                location=self.config['country'],
                company=self.config['advertiser']
                )
      else:
        return (
            prompts[self.config['language']]['GENERATION']
            ['WITHOUT_ASSOCIATIVE_TERM']['WITH_DESCRIPTION']
            ).format(
                n=number_of_copies,
                length=length,
                term=entry.term,
                term_description=entry.term_description,
                location=self.config['country'],
                company=self.config['advertiser']
                )
    elif (
        entry.term_description
        and entry.associative_term_description
        ):
      return (
          prompts[self.config['language']]['GENERATION']
          ['WITH_ASSOCIATIVE_TERM']['WITH_BOTH_DESCRIPTIONS']
          ).format(
              n=number_of_copies,
              length=length,
              term=entry.term,
              term_description=entry.term_description,
              associative_term=entry.associative_term,
              associative_term_description=entry.associative_term_description,
              location=self.config['country'],
              company=self.config['advertiser'],
              association_reason=entry.association_reason
              )
    elif (
        entry.term_description
        and not entry.associative_term_description
        ):
      return (
          prompts[self.config['language']]['GENERATION']
          ['WITH_ASSOCIATIVE_TERM']['WITH_TERM_DESCRIPTION']
          ).format(
              n=number_of_copies,
              length=length,
              term=entry.term,
              term_description=entry.term_description,
              associative_term=entry.associative_term,
              location=self.config['country'],
              company=self.config['advertiser'],
              association_reason=entry.association_reason
              )
    elif (
        not entry.term_description and
        entry.associative_term_description
        ):
      return (
          prompts[self.config['language']]['GENERATION']
          ['WITH_ASSOCIATIVE_TERM']['WITH_ASSOCIATIVE_TERM_DESCRIPTION']
          ).format(
              n=number_of_copies,
              length=length,
              term=entry.term,
              associative_term=entry.associative_term,
              associative_term_description=entry.associative_term_description,
              location=self.config['country'],
              company=self.config['advertiser'],
              association_reason=entry.association_reason
              )
    elif (
        not entry.term_description and
        not entry.associative_term_description
        ):
      return (
          prompts[self.config['language']]['GENERATION']
          ['WITH_ASSOCIATIVE_TERM']['WITHOUT_DESCRIPTIONS']
          ).format(
              n=number_of_copies,
              length=length,
              term=entry.term,
              associative_term=entry.associative_term,
              location=self.config['country'],
              company=self.config['advertiser'],
              association_reason=entry.association_reason
              )
