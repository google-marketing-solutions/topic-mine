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

"""Entry class.
"""

import uuid


class Entry:
  """Entry class. Combination of term and associative_term with copies.
  """
  id: str
  sku: str
  url: str
  image_url: str
  term: str
  term_description: str
  associative_term: str
  associative_term_description: str
  association_reason: str
  relationship: bool
  headlines: list[str]
  descriptions: list[str]
  keywords: list[str]
  paths: list[str]

  def __init__(
      self,
      term: str,
      term_description: str = None,
      associative_term: str = None,
      associative_term_description: str = None,
      sku: str = None,
      url: str = None,
      image_url: str = None
      ):
    self.term = term
    self.term_description = term_description
    self.associative_term = associative_term
    self.associative_term_description = associative_term_description
    self.sku = sku
    self.url = url
    self.image_url = image_url

    self.id = uuid.uuid4()
    self.association_reason = None
    self.relationship = False
    self.headlines = None
    self.descriptions = None
    self.keywords = None
    self.paths = None

  def __str__(self):
    return (
        '[term: ' + self.term + ', associative_term: ' + self.associative_term +
        ', association_reason: ' + self.association_reason + ', headlines: ' +
        str(self.headlines) + ', descriptions: ' + str(self.descriptions) +
        ', keywords: ' + str(self.keywords) + ', paths: ' + str(self.paths) + ']'
        )

  def must_generate_content(self, must_find_relationship: bool):
    """True if content must be generated for this entry, otherwise false.

    Args:
      must_find_relationship (bool): If an association between
      first_term and second_term must be found.

    Returns:
      bool: If content must be generated or not.
    """
    if (
        self.term is not None and self.associative_term is not None
        and not must_find_relationship
        ):
      return True
    elif (
        self.term is not None and self.associative_term is not None
        and must_find_relationship
        ):
      return self.relationship
    elif self.term is not None and self.associative_term is None:
      return True

    return False

  def has_associative_term(self):
    """True if associative_term is present, otherwise false.

    Returns:
      bool: If associative_term is present or not.
    """
    return self.associative_term is not None

  def must_be_exported(self):
    """True if entry must be exported, otherwise false.

    Returns:
      bool: If entry must be exported or not.
    """
    return (
        self.headlines is not None and self.headlines and
        self.descriptions is not None and self.descriptions and
        self.keywords is not None and self.keywords and
        self.paths is not None and self.paths
        )
