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

"""SA360 Feed Row class.

It transforms and loads data to a Google sheet
with the correct format of an DV360 feed.
"""


class SA360FeedRow:
  """SA360 Feed Row class.

  It transforms and loads data to a Google sheet
  with the correct format of an DV360 feed.
  """
  row_id: str
  publish: str
  trend: str
  term: str
  relationship: str
  reason: str
  sku: str
  keywords: list[str]
  url: str
  headlines: list[str]
  descriptions: list[str]
  paths: list[str]
  campaign_id: str
  ad_group_id: str

  def __init__(
      self,
      row_id: str,
      publish: str,
      trend: str,
      term: str,
      relationship: bool,
      reason: str,
      sku: str,
      keywords: list[str],
      url: str,
      headlines: list[str],
      descriptions: list[str],
      paths: list[str],
      campaign_id: int,
      ad_group_id: int,
  ):
    """Init method for SA360FeedRow."""
    self.row_id = row_id
    self.publish = publish
    self.trend = trend
    self.term = term
    self.relationship = relationship
    self.reason = reason
    self.sku = sku
    self.keywords = keywords
    self.url = url
    self.headlines = headlines
    self.descriptions = descriptions
    self.paths = paths
    self.campaign_id = campaign_id
    self.ad_group_id = ad_group_id
