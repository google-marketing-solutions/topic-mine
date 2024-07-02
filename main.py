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

"""Main module.
"""

import logging
import os
import threading
from typing import Any

from flask import Flask
from flask import jsonify
from flask import request
from output_writers.acs_feed_destination import ACSFeedDestination
from output_writers.dv360_feed_destination import DV360FeedDestination
from output_writers.sa360_feed_destination import SA360FeedDestination
from services.content_generator_service import ContentGeneratorService
from utils.entry import Entry
from utils.enums import Destination
from utils.enums import FirstTermSource
from utils.enums import SecondTermSource
from utils.utils import Utils

app = Flask(__name__)

# Logger config
logging.basicConfig()
logging.root.setLevel(logging.INFO)

# Helpers and config
config = Utils.load_config('config.json')

content_generator_service = ContentGeneratorService(config)


tasks = {}
task_id = 0


@app.route('/tasks/<int:tid>', methods=['GET'])
def get_task_status(tid):
  """Get status given a task id.

  Args:
    tid(int): The task id to retrieve status of.

  Returns:
    A JSON response with the status.
  """
  if tid not in tasks:
    return jsonify({'error': 'Task not found'}), 404

  return jsonify(tasks[tid]), 200


@app.route('/content', methods=['POST'])
def start_task():
  """App's entry point.

  Validates params and returns accordingly..

  Returns:
    A JSON response with a success message and a 202 status code if params ok
    and generation started.
    A JSON response with an error message and a 400 status code if user error.
    A JSON response with an error message and a 500 status code if bt failure.
  """
  global task_id

  try:
    if task_id in tasks and tasks[task_id]['status'] == 'running':
      return jsonify({'error': 'Task already running'}), 409

    destination = __get_destination(request)
    first_term_source = __get_first_term_source(request)
    second_term_source = __get_second_term_source(request)
    must_find_relationship = __get_must_find_relationship(request)
    body_params = __validate_body_params(
        request,
        destination,
        first_term_source,
        second_term_source
        )

    task_id += 1

    threading.Thread(
        target=__generate_and_export_content,
        args=(task_id,
              first_term_source,
              second_term_source,
              must_find_relationship,
              body_params,
              destination
             )
        ).start()
  except ValueError as e:
    logging.error(' %s', str(e))
    tasks[task_id] = {'status': 'failed 400', 'result': str(e)}
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    logging.error(' %s', str(e))
    tasks[task_id] = {'status': 'failed 500', 'result': str(e)}
    return jsonify({'error': str(e)}), 500

  tasks[task_id] = {'status': 'running'}

  logging.info(' Task %s started', task_id)
  return jsonify({'status': 'accepted', 'task_id': task_id}), 202


def __generate_and_export_content(
    tid: int,
    first_term_source: FirstTermSource,
    second_term_source: SecondTermSource | None,
    must_find_relationship: bool,
    body_params: dict[str, Any],
    destination: Destination
):
  """Generates and exports content.

  Args:
    tid(int): New task id.
    first_term_source(FirstTermSource): The first term source.
    second_term_source(SecondTermSource): The second term source.
    must_find_relationship(bool): Whether to find a relationship.
    body_params (dict[str, Any]): The params of the request.
    destination(Destination): The destination output.
  """
  try:
    entries = content_generator_service.generate_content(
        first_term_source,
        second_term_source,
        must_find_relationship,
        body_params
        )

    __export_entries(entries, destination, body_params)

    tasks[tid] = {'status': 'completed', 'result': 'ok'}
  except Exception as e:
    logging.error(' %s', str(e))
    tasks[tid] = {'status': 'failed 500', 'result': str(e)}


def __get_destination(r) -> Destination:
  """Validate and get the destination query param.

  Args:
    r: The request object.

  Returns:
    str: The destination query param.

  Raises:
    ValueError: If the destination query param is invalid.
  """
  destination = r.args.get('destination')

  match destination:
    case 'dv360feed':
      return Destination.DV360_FEED
    case 'sa360feed':
      return Destination.SA360_FEED
    case 'acsfeed':
      return Destination.ACS_FEED
    case 'dv360':
      raise ValueError('Destination dv360 not yet supported')
      # return Destination.DV360_API
    case 'sa360':
      raise ValueError('Destination sa360 not yet supported')
      # return Destination.SA360_API
    case _:
      raise ValueError(
          'Invalid destination query param.' +
          'Supported values are dv360feed, sa360feed, dv360, sa360.'
          )


def __get_first_term_source(r) -> FirstTermSource:
  """Validate and get the first-term-source query param.

  Args:
    r: The request object.

  Returns:
    str: The first-term-source query param.

  Raises:
    ValueError: If the first-term-source query param is invalid.
  """
  first_term_source = r.args.get('first-term-source')

  if not first_term_source or first_term_source not in [
      'spreadsheet',
      'big_query'
      ]:
    raise ValueError(
        'Invalid first-term-source query param.'+
        'Supported values are spreadsheet and big_query.'
        )

  if first_term_source == 'spreadsheet':
    first_term_source = FirstTermSource.SPREADSHEET
  elif first_term_source == 'big_query':
    first_term_source = FirstTermSource.BIG_QUERY

  return first_term_source


def __get_second_term_source(r) -> SecondTermSource:
  """Validate and get the second-term-source query param.

  Args:
    r: The request object.

  Returns:
    str: The second-term-source query param.

  Raises:
    ValueError: If the second-term-source query param is invalid.
  """
  second_term_source = r.args.get('second-term-source')

  if second_term_source and second_term_source not in [
      'google_trends',
      'search_scout',
      'rss_feed',
      'spreadsheet'
      ]:
    raise ValueError(
        'Invalid second-term-source query param. Supported values are '+
        'none (no param), google_trends, search_scout, rss_feed.'
        )

  if second_term_source == 'google_trends':
    second_term_source = SecondTermSource.GOOGLE_TRENDS
  elif second_term_source == 'search_scout':
    second_term_source = SecondTermSource.SEARCH_SCOUT
  elif second_term_source == 'rss_feed':
    second_term_source = SecondTermSource.RSS_FEED
  elif second_term_source == 'spreadsheet':
    second_term_source = SecondTermSource.SPREADSHEET
  elif second_term_source is None:
    second_term_source = SecondTermSource.NONE

  return second_term_source


def __get_must_find_relationship(r) -> bool:
  """Validate and get the must-find-relationship query param.

  Args:
    r: The request object.

  Returns:
    str: The must-find-relationship query param.

  Raises:
    ValueError: If the must-find-relationship query param is invalid.
  """
  second_term_source = r.args.get('second-term-source')
  must_find_relationship = r.args.get('must-find-relationship')

  if (
      (not second_term_source and must_find_relationship) or
      (second_term_source and not (
          must_find_relationship == 'true' or must_find_relationship == 'false'
          )
      )
    ):
    raise ValueError(
        'Invalid must-find-relationship query param. Supported values '+
        'are true or false only if second-term-source is specified.'
        )

  if second_term_source:
    return must_find_relationship.lower() == 'true'
  else:
    return False


def __validate_body_params(
    r,
    destination: Destination,
    first_term_source: FirstTermSource,
    second_term_source: SecondTermSource
    ) -> dict[str, Any]:
  """Validate and get the body params.

  Args:
    r: The request object.
    destination(Destination): The destination query param.
    first_term_source(FirstTermSource): The first-term-source query param.
    second_term_source(SecondTermSource): The second-term-source query param.

  Returns:
    dict[str, Any]: The body params.

  Raises:
    ValueError: If the body params are invalid.
  """
  data = r.get_json()

  if data is None:
    raise ValueError('Missing body params.')

  if ('url_validation' in data
      and data['url_validation'] == 'USE_DEFAULT_URL'
      and 'default_url' not in data):
    raise ValueError('Missing default_url body param.')

  if 'num_headlines' not in data:
    raise ValueError('Missing num_headlines body param.')
  elif not isinstance(data['num_headlines'], int):
    raise ValueError('Invalid num_headlines body param, must be of type int.')

  if 'num_descriptions' not in data:
    raise ValueError('Missing num_descriptions body param.')
  elif not isinstance(data['num_descriptions'], int):
    raise ValueError('Invalid num_descriptions body param, must be type int.')

  if 'first_term_source_config' not in data:
    raise ValueError('Missing first_term_source_config body param.')

  if first_term_source == FirstTermSource.SPREADSHEET:
    if 'spreadsheet_id' not in data['first_term_source_config']:
      raise ValueError('Missing spreadsheet_id in first_term_source_config.')
    if 'sheet_name' not in data['first_term_source_config']:
      raise ValueError('Missing sheet_name in first_term_source_config.')
    if (
        'starting_row' not in data['first_term_source_config'] or
        not isinstance(data['first_term_source_config']['starting_row'], int)
        ):
      raise ValueError('Missing or invalid starting_row in first_term_source_config. Must be int.')
    if 'term_column' not in data['first_term_source_config']:
      raise ValueError('Missing term_column in first_term_source_config.')
    if (
        'limit' not in data['first_term_source_config'] or
        not isinstance(data['first_term_source_config']['limit'], int)
        ):
      raise ValueError('Missing or invalid limit in first_term_source_config. Must be of type int.')
    if data['first_term_source_config']['limit'] == 0:
      data['first_term_source_config']['limit'] = 9999
  elif first_term_source == FirstTermSource.BIG_QUERY:
    if 'query' not in data['first_term_source_config']:
      if 'project_id' not in data['first_term_source_config']:
        raise ValueError('Missing project_id in first_term_source_config.')
      if 'dataset' not in data['first_term_source_config']:
        raise ValueError('Missing dataset in first_term_source_config.')
      if 'table' not in data['first_term_source_config']:
        raise ValueError('Missing table in first_term_source_config.')
      if 'term_column' not in data['first_term_source_config']:
        raise ValueError('Missing term_column in first_term_source_config.')
      if (
          'limit' not in data['first_term_source_config'] or
          not isinstance(data['first_term_source_config']['limit'], int)
          ):
        raise ValueError('Missing or invalid limit in first_term_source_config. Must be of type int.')
      if data['first_term_source_config']['limit'] == 0:
        data['first_term_source_config']['limit'] = 9999

  if (
      'second_term_source_config' in data and
      second_term_source == SecondTermSource.NONE
      ):
    raise ValueError('Invalid second_term_source_config body param.')
  elif (
      'second_term_source_config' not in data and
      second_term_source != SecondTermSource.NONE
      ):
    raise ValueError('Missing second_term_source_config body param.')

  if second_term_source == SecondTermSource.NONE:
    pass
  elif second_term_source == SecondTermSource.GOOGLE_TRENDS:
    if (
        'limit' not in data['second_term_source_config'] or
        not isinstance(data['second_term_source_config']['limit'], int)
        ):
      raise ValueError('Missing or invalid limit in second_term_source_config. Must be of type int.')
    if data['second_term_source_config']['limit'] == 0:
      data['second_term_source_config']['limit'] = 9999
  elif second_term_source == SecondTermSource.SEARCH_SCOUT:
    if 'project_id' not in data['second_term_source_config']:
      raise ValueError('Missing project_id in second_term_source_config.')
    if 'dataset' not in data['second_term_source_config']:
      raise ValueError('Missing dataset in second_term_source_config.')
    if 'table' not in data['second_term_source_config']:
      raise ValueError('Missing table in second_term_source_config.')
    if 'term_column' not in data['second_term_source_config']:
      raise ValueError('Missing term_column in second_term_source_config.')
    if (
        'limit' not in data['second_term_source_config'] or
        not isinstance(data['second_term_source_config']['limit'], int)
        ):
      raise ValueError('Missing or invalid limit in second_term_source_config. Must be of type int.')
    if data['second_term_source_config']['limit'] == 0:
      data['second_term_source_config']['limit'] = 9999
  elif second_term_source == SecondTermSource.RSS_FEED:
    # TODO: TBD
    pass
  elif second_term_source == SecondTermSource.SPREADSHEET:
    if 'spreadsheet_id' not in data['second_term_source_config']:
      raise ValueError('Missing spreadsheet_id in second_term_source_config.')
    if 'sheet_name' not in data['second_term_source_config']:
      raise ValueError('Missing sheet_name in second_term_source_config.')
    if (
        'starting_row' not in data['second_term_source_config'] or
        not isinstance(data['second_term_source_config']['starting_row'], int)
        ):
      raise ValueError('Missing or invalid starting_row in second_term_source_config. Must be of type int.')
    if 'term_column' not in data['second_term_source_config']:
      raise ValueError('Missing term_column in second_term_source_config.')
    if (
        'limit' not in data['second_term_source_config'] or
        not isinstance(data['second_term_source_config']['limit'], int)
        ):
      raise ValueError('Missing or invalid limit in second_term_source_config. Must be of type int.')
    if data['second_term_source_config']['limit'] == 0:
      data['second_term_source_config']['limit'] = 9999

  if (
      destination == Destination.SA360_FEED or
      destination == Destination.DV360_FEED
      ):
    if 'destination_config' not in data:
      raise ValueError('Missing destination_config body param.')
    if 'spreadsheet_id' not in data['destination_config']:
      raise ValueError('Missing spreadsheet_id in destination_config.')
    if 'sheet_name' not in data['destination_config']:
      raise ValueError('Missing sheet_name in destination_config.')
  elif destination == Destination.SA360_API:
    # TODO: TBD
    pass
  elif destination == Destination.DV360_API:
    # TODO: TBD
    pass
  elif destination == Destination.ACS_FEED:
    if 'destination_config' not in data:
      raise ValueError('Missing destination_config body param.')
    if 'spreadsheet_id' not in data['destination_config']:
      raise ValueError('Missing spreadsheet_id in destination_config.')
    if 'sheet_name' not in data['destination_config']:
      raise ValueError('Missing sheet_name in destination_config.')
    if 'variant_name_column' not in data['destination_config']:
      raise ValueError('Missing variant_name_column in destination_config.')
    if (
        'constant_columns' not in data['destination_config'] or
        not isinstance(data['destination_config']['constant_columns'], list)
        ):
      raise ValueError('Missing constant_columns in destination_config.')
    if (
        'copies_columns' not in data['destination_config'] or
        not isinstance(data['destination_config']['copies_columns'], list)
        ):
      raise ValueError('Missing copies_columns in destination_config.')
    if (
        'starting_row' not in data['destination_config'] or
        not isinstance(data['destination_config']['starting_row'], int)
        ):
      raise ValueError('Missing or invalid starting_row in destination_config. Must be of type int.')

  return data


def __export_entries(entries: list[Entry], destination: Destination, body_params: dict[str, Any]):
  """Export the entries to the destination.

  Args:
    entries (list[Entry]): The entries to export.
    destination(Destination): The destination query param.
    body_params (dict[str, Any]): The body params.

  Returns:
    str: The destination query param.
  """
  logging.info(' Exporting content...')
  if destination == Destination.SA360_FEED:
    sa360_feed_destination = SA360FeedDestination(config)
    sheet_id = body_params['destination_config']['spreadsheet_id']
    sheet_name = body_params['destination_config']['sheet_name']
    sa360_feed_destination.write_destination_output(
        entries,
        sheet_id,
        sheet_name
        )
  elif destination == Destination.DV360_FEED:
    sheet_id = body_params['destination_config']['spreadsheet_id']
    sheet_name = body_params['destination_config']['sheet_name']
    dv360_feed_destination = DV360FeedDestination(config)
    dv360_feed_destination.write_destination_output(
        entries,
        sheet_id,
        sheet_name
        )
  elif destination == Destination.ACS_FEED:
    sheet_id = body_params['destination_config']['spreadsheet_id']
    sheet_name = body_params['destination_config']['sheet_name']
    variant_name_column = body_params['destination_config']['variant_name_column']
    constant_columns = body_params['destination_config']['constant_columns']
    copies_columns = body_params['destination_config']['copies_columns']
    starting_row = body_params['destination_config']['starting_row']
    acs_feed_destination = ACSFeedDestination(config)
    acs_feed_destination.write_destination_output(
        entries,
        sheet_id,
        sheet_name,
        variant_name_column,
        constant_columns,
        copies_columns,
        starting_row
        )
  elif destination == Destination.SA360_API:
    pass
    # TODO: export to sa360
  elif destination == Destination.DV360_API:
    pass
    # TODO: export to dv360
  logging.info(' Content exported!')


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
