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

"""DV360 Feed Row class.

It transforms and loads data to a Google sheet
with the correct format of an DV360 feed.
"""

import uuid

# TODO: REMOVE CLASS
class DV360FeedRow:
  """DV360 Feed Row class.

  It transforms and loads data to a Google sheet
  with the correct format of an DV360 feed.
  """

  id: str
  sku: str
  term: str
  term_description: str
  associative_term: str
  associative_term_description: str
  url: str
  image_url: str
  association_reason: str
  relationship: bool
  headlines: list[str]
  descriptions: list[str]
  keywords: list[str]
  active: str
  default: str

  def __init__(
      self,
      term: str,
      term_description: str | None,
      sku: str | None,
      associative_term: str | None,
      associative_term_description: str | None,
      url: str | None,
      image_url: str | None,
      association_reason: str | None,
      relationship: bool | None,
      headlines: list[str],
      descriptions: list[str],
      keywords: list[str]
      ):
    """Init method for DV360FeedRow."""
    self.id = str(uuid.uuid4())
    self.term = term
    self.term_description = term_description
    self.sku = sku
    self.associative_term = associative_term
    self.associative_term_description = associative_term_description
    self.url = url
    self.image_url = image_url
    self.association_reason = association_reason
    self.relationship = relationship
    self.headlines = headlines
    self.descriptions = descriptions
    self.keywords = keywords
    self.active = ''
    self.default = ''
