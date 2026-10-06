# Copyright 2026 Google LLC
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

"""Unit tests for BigQuery security validation and arbitrary query remediation."""

import sys
import unittest
from unittest.mock import MagicMock

import types

class MockPackage(MagicMock):
  __path__ = []

# Mock packages and modules before importing project modules
packages = [
    'google', 'google.cloud', 'google.ads', 'google.ads.googleads',
    'google.auth', 'google.oauth2', 'google_auth_oauthlib',
    'vertexai'
]
for pkg in packages:
  if pkg not in sys.modules:
    sys.modules[pkg] = MockPackage()

modules = [
    'google.cloud.bigquery',
    'google.cloud.aiplatform',
    'google.ads.googleads.client',
    'google.auth.transport.requests',
    'google.oauth2.credentials',
    'google_auth_oauthlib.flow',
    'vertexai.generative_models',
    'flask', 'pandas', 'gspread', 'dirtyjson',
    'alive_progress', 'google.generativeai', 'validators', 'backoff',
    'requests'
]
for mod in modules:
  if mod not in sys.modules:
    sys.modules[mod] = MagicMock()

# Ensure Flask class and request can be used
mock_flask = sys.modules['flask']
mock_flask.Flask = MagicMock()

from utils.utils import Utils
from utils.enums import Destination, FirstTermSource, SecondTermSource
from utils.bigquery_helper import BigQueryHelper
import main


class TestBigQuery(unittest.TestCase):
  """Tests verifying BigQuery validation, operations, and security remediation."""

  def test_is_valid_bigquery_identifier_valid(self):
    """Test valid BigQuery table, dataset, and column identifiers."""
    self.assertTrue(Utils.is_valid_bigquery_identifier('valid_column'))
    self.assertTrue(Utils.is_valid_bigquery_identifier('dataset_123'))
    self.assertTrue(Utils.is_valid_bigquery_identifier('table_name'))
    self.assertTrue(Utils.is_valid_bigquery_identifier('table-with-hyphens', allow_hyphen=True))
    self.assertFalse(Utils.is_valid_bigquery_identifier('table-with-hyphens', allow_hyphen=False))

  def test_is_valid_bigquery_identifier_injection_payloads(self):
    """Test that malicious SQL injection payloads are rejected."""
    malicious_inputs = [
        'column; DROP TABLE users;--',
        'col` FROM `sensitive_table`--',
        'col UNION SELECT * FROM passwords',
        'table` WHERE 1=1--',
        'column/**/name',
        'col\nFROM table',
        '',
        None,
        123,
        'a' * 1025,  # Exceeds max length
    ]
    for payload in malicious_inputs:
      with self.subTest(payload=payload):
        self.assertFalse(Utils.is_valid_bigquery_identifier(payload, allow_hyphen=True))
        self.assertFalse(Utils.is_valid_bigquery_identifier(payload, allow_hyphen=False))

  def test_is_valid_project_id(self):
    """Test GCP project ID validation."""
    self.assertTrue(Utils.is_valid_project_id('my-project-123'))
    self.assertTrue(Utils.is_valid_project_id('google.com:my-project'))
    self.assertTrue(Utils.is_valid_project_id('project_under_score'))

    # Malicious inputs
    self.assertFalse(Utils.is_valid_project_id('proj` DROP TABLE users;'))
    self.assertFalse(Utils.is_valid_project_id('proj UNION SELECT 1'))
    self.assertFalse(Utils.is_valid_project_id('proj; SELECT *'))
    self.assertFalse(Utils.is_valid_project_id(''))
    self.assertFalse(Utils.is_valid_project_id(None))
    self.assertFalse(Utils.is_valid_project_id('a' * 101))

  def test_read_bigquery_column_validation(self):
    """Test that BigQueryHelper.read_bigquery_column validates identifiers."""
    helper = object.__new__(BigQueryHelper)
    helper.bigquery_client = MagicMock()

    # Invalid project ID
    with self.assertRaises(ValueError) as ctx:
      helper.read_bigquery_column('proj` injection', 'dataset', 'table', 'col', 10)
    self.assertIn('Invalid project_id', str(ctx.exception))

    # Invalid dataset ID
    with self.assertRaises(ValueError) as ctx:
      helper.read_bigquery_column('valid-proj', 'data;set', 'table', 'col', 10)
    self.assertIn('Invalid dataset_id', str(ctx.exception))

    # Invalid table ID
    with self.assertRaises(ValueError) as ctx:
      helper.read_bigquery_column('valid-proj', 'dataset', 'table`-- ', 'col', 10)
    self.assertIn('Invalid table_id', str(ctx.exception))

    # Invalid column name
    with self.assertRaises(ValueError) as ctx:
      helper.read_bigquery_column('valid-proj', 'dataset', 'table', 'col` FROM sensitive', 10)
    self.assertIn('Invalid column_name', str(ctx.exception))

    # Invalid limit
    with self.assertRaises(ValueError) as ctx:
      helper.read_bigquery_column('valid-proj', 'dataset', 'table', 'col', 0)
    self.assertIn('Invalid limit', str(ctx.exception))

    # Valid execution
    mock_row = {'col': 'val1'}
    helper.bigquery_client.query.return_value.result.return_value = [mock_row]
    result = helper.read_bigquery_column('valid-proj', 'valid_dataset', 'valid_table', 'col', 10)
    self.assertEqual(result, ['val1'])
    helper.bigquery_client.query.assert_called_once_with(
        'SELECT col FROM `valid-proj.valid_dataset.valid_table` LIMIT 10'
    )

  def test_main_rejects_raw_query_in_first_term_source_config(self):
    """Test that passing 'query' in first_term_source_config is rejected with ValueError."""
    validate_func = getattr(main, '_main__validate_body_params', getattr(main, '__validate_body_params', None))
    self.assertIsNotNone(validate_func, 'Could not find __validate_body_params in main module')

    mock_req = MagicMock()
    mock_req.get_json.return_value = {
        'num_headlines': 3,
        'num_descriptions': 2,
        'first_term_source_config': {
            'query': 'SELECT * FROM `confidential_dataset.secret_table`'
        }
    }

    with self.assertRaises(ValueError) as ctx:
      validate_func(
          mock_req,
          Destination.ACS_FEED,
          FirstTermSource.BIG_QUERY,
          SecondTermSource.NONE
      )
    self.assertIn('Arbitrary BigQuery queries via "query" parameter are not supported', str(ctx.exception))

  def test_main_rejects_sql_injection_in_structured_fields(self):
    """Test that SQL injection in structured BigQuery config fields is rejected."""
    validate_func = getattr(main, '_main__validate_body_params', getattr(main, '__validate_body_params', None))

    test_cases = [
        ('project_id', 'proj` --', 'Invalid project_id'),
        ('dataset', 'dataset; DROP TABLE', 'Invalid dataset'),
        ('table', 'table` UNION SELECT', 'Invalid table'),
        ('term_column', 'term` FROM passwords--', 'Invalid term_column'),
        ('term_description_column', 'desc`--', 'Invalid term_description_column'),
        ('sku_column', 'sku;--', 'Invalid sku_column'),
        ('url_column', 'url`--', 'Invalid url_column'),
        ('image_url_column', 'img`--', 'Invalid image_url_column'),
    ]

    for field, mal_value, expected_msg in test_cases:
      with self.subTest(field=field, value=mal_value):
        config = {
            'project_id': 'valid-proj',
            'dataset': 'valid_dataset',
            'table': 'valid_table',
            'term_column': 'valid_term',
            'limit': 100
        }
        config[field] = mal_value
        mock_req = MagicMock()
        mock_req.get_json.return_value = {
            'num_headlines': 3,
            'num_descriptions': 2,
            'first_term_source_config': config
        }
        with self.assertRaises(ValueError) as ctx:
          validate_func(
              mock_req,
              Destination.ACS_FEED,
              FirstTermSource.BIG_QUERY,
              SecondTermSource.NONE
          )
        self.assertIn(expected_msg, str(ctx.exception))

  def test_main_accepts_valid_structured_bigquery_config(self):
    """Test that a valid structured BigQuery config passes validation."""
    validate_func = getattr(main, '_main__validate_body_params', getattr(main, '__validate_body_params', None))

    mock_req = MagicMock()
    mock_req.get_json.return_value = {
        'num_headlines': 3,
        'num_descriptions': 2,
        'first_term_source_config': {
            'project_id': 'my-valid-project',
            'dataset': 'marketing_dataset',
            'table': 'product_terms_2026',
            'term_column': 'product_name',
            'term_description_column': 'description',
            'sku_column': 'sku_id',
            'url_column': 'landing_url',
            'image_url_column': 'image_url',
            'limit': 50
        },
        'destination_config': {
            'spreadsheet_id': 'valid_sheet_id',
            'sheet_name': 'valid_sheet_name'
        }
    }

    result = validate_func(
        mock_req,
        Destination.SA360_FEED,
        FirstTermSource.BIG_QUERY,
        SecondTermSource.NONE
    )
    self.assertEqual(result['first_term_source_config']['project_id'], 'my-valid-project')
    self.assertEqual(result['first_term_source_config']['limit'], 50)

  def test_main_rejects_invalid_limit(self):
    """Test that negative, non-integer, or missing limits are rejected."""
    validate_func = getattr(main, '_main__validate_body_params', getattr(main, '__validate_body_params', None))

    invalid_limits = [-1, -999, '100', None, 1.5]
    for limit in invalid_limits:
      with self.subTest(limit=limit):
        mock_req = MagicMock()
        mock_req.get_json.return_value = {
            'num_headlines': 3,
            'num_descriptions': 2,
            'first_term_source_config': {
                'project_id': 'valid-proj',
                'dataset': 'valid_dataset',
                'table': 'valid_table',
                'term_column': 'valid_term',
                'limit': limit
            },
            'destination_config': {
                'spreadsheet_id': 'sheet1',
                'sheet_name': 'Sheet1'
            }
        }
        with self.assertRaises(ValueError) as ctx:
          validate_func(
              mock_req,
              Destination.SA360_FEED,
              FirstTermSource.BIG_QUERY,
              SecondTermSource.NONE
          )
        self.assertIn('limit', str(ctx.exception).lower())

  def test_main_search_scout_validation(self):
    """Test that Search Scout (SecondTermSource) validates BigQuery identifiers."""
    validate_func = getattr(main, '_main__validate_body_params', getattr(main, '__validate_body_params', None))

    # Test rejection of injection in Search Scout
    mock_req = MagicMock()
    mock_req.get_json.return_value = {
        'num_headlines': 3,
        'num_descriptions': 2,
        'first_term_source_config': {
            'project_id': 'valid-proj',
            'dataset': 'valid_dataset',
            'table': 'valid_table',
            'term_column': 'valid_term',
            'limit': 10
        },
        'second_term_source_config': {
            'project_id': 'valid-proj',
            'dataset': 'valid_dataset',
            'table': 'table` DROP TABLE users;--',
            'term_column': 'term',
            'limit': 10
        },
        'destination_config': {
            'spreadsheet_id': 'sheet1',
            'sheet_name': 'Sheet1'
        }
    }
    with self.assertRaises(ValueError) as ctx:
      validate_func(
          mock_req,
          Destination.SA360_FEED,
          FirstTermSource.BIG_QUERY,
          SecondTermSource.SEARCH_SCOUT
      )
    self.assertIn('Invalid table in second_term_source_config', str(ctx.exception))

  def test_content_generator_service_bq_reads_structured(self):
    """Test that ContentGeneratorService retrieves terms using structured read instead of raw query."""
    from services.content_generator_service import ContentGeneratorService
    service = object.__new__(ContentGeneratorService)
    service.bigquery_helper = MagicMock()
    service.bigquery_helper.read_bigquery_column.side_effect = [
        ['term1', 'term2'],  # terms
        ['desc1', 'desc2'],  # descriptions
        ['sku1', 'sku2'],    # skus
        ['url1', 'url2'],    # urls
        ['img1', 'img2'],    # image_urls
    ]
    service.body_params = {
        'first_term_source_config': {
            'project_id': 'test-project',
            'dataset': 'test_dataset',
            'table': 'test_table',
            'term_column': 'term',
            'term_description_column': 'description',
            'sku_column': 'sku',
            'url_column': 'url',
            'image_url_column': 'image_url',
            'limit': 10
        }
    }

    terms, descs, skus, urls, imgs = getattr(service, '_ContentGeneratorService__get_first_term_info_from_bq')()
    self.assertEqual(terms, ['term1', 'term2'])
    self.assertEqual(descs, ['desc1', 'desc2'])
    self.assertEqual(skus, ['sku1', 'sku2'])
    self.assertEqual(urls, ['url1', 'url2'])
    self.assertEqual(imgs, ['img1', 'img2'])
    # Ensure run_query was never called
    service.bigquery_helper.run_query.assert_not_called()


if __name__ == '__main__':
  unittest.main()
