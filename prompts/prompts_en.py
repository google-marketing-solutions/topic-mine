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

prompts_en = {
  'ASSOCIATION': {
    'WITH_BOTH_DESCRIPTIONS': "Tell me if you find a direct or indirect relationship between '{term}', which's description is '{term_description}', and '{associative_term}', which's description is '{associative_term_description}'.",
    'WITH_TERM_DESCRIPTION': "Tell me if you find a direct or indirect relationship between '{term}', which's description is '{term_description}', and '{associative_term}'.",
    'WITH_ASSOCIATIVE_TERM_DESCRIPTION': "Tell me if you find a direct or indirect relationship between '{term}' and '{associative_term}', which's description is '{associative_term_description}'.",
    'WITHOUT_DESCRIPTIONS': "Tell me if you find a direct or indirect relationship between '{term}' and '{associative_term}'.",
    'COMMON_PART':  """
                    If there is any way to associate them, even if it is not very clear, it already means they are related.

                                    Response must be in JSON format, following this example:
                                    {{"term": "{term}", "associative_term": "{associative_term}", "relationship": true/false, "reason": "reason why there is or isn't relationship between {term} and {associative_term}"}}
                    """,
  },
  'GENERATION': {
    'WITH_ASSOCIATIVE_TERM': {
      'WITH_TERM_DESCRIPTION':  """
                                Generate {n} texts of less than {length} characters for a Google Ads ad.
                                This ad has to be related with the terms '{term}', which's description is '{term_description}', and '{associative_term}'.
                                  They must incentive the reader to buy '{term}' because '{association_reason}' is trending.
                                  Consider the following association reason between the two terms: '{association_reason}'.
                                  It is extremely important that they are as short as possible, they must be shorter than {length} characters.
                                  Try to include key words related with the trending topic in the texts.
                                  If the generated texts are long, try to include the retailer's name, which is {company}, in the texts.

                                  Response must be in exactly the following format:
                                  ["write here the text 1", "write here the text 2", ..., "write here the text {n}"]
                                  The response must follow exactly that format. It does not have to contain any additional commas, whitespaces or line breaks. It must be just a comma-separated list of texts between square brackets and thats it.
                                  """
    },
  },
  'SIZE_ENFORCEMENT': """
                    I will give you one text for a Google Ads ad that is too long.
                    Make it shorter, it has to be shorter than {max_length} characters.
                    The text is: {copy}

                    Give me the response like this:
                    shortened_text
                    Just give me as a response the shortened text without quotation marks, line breaks or anything else.
                    """
}