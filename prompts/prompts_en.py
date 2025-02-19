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
    "ASSOCIATION": {
        "WITH_BOTH_DESCRIPTIONS": """
    Tell me if there is a direct or indirect relationship between '{term}', whose description is '{term_description}',
    and '{associative_term}' whose description is '{associative_term_description}'.
  """,
        "WITH_TERM_DESCRIPTION": """
    Tell me if there is a direct or indirect relationship between '{term}', whose description is '{term_description}',
    and '{associative_term}'.
  """,
        "WITH_ASSOCIATIVE_TERM_DESCRIPTION": """
    Tell me if there is a direct or indirect relationship between '{term}' and '{associative_term}',
    whose description is '{associative_term_description}'.
  """,
        "WITHOUT_DESCRIPTIONS": """
    Tell me if there is a direct or indirect relationship between '{term}' and '{associative_term}'.
  """,
        "COMMON_PART": """
    Find if there is any way to associate the terms, even if it is not a very direct relationship.

    Response must be in JSON format, following this example:
    {{"term": "{term}", "associative_term": "{associative_term}", "relationship": true/false, "reason": "reason why there is or isn't relationship between {term} and {associative_term}"}}
  """,
    },
    "GENERATION": {
        "WITH_ASSOCIATIVE_TERM": {
            "WITHOUT_RELATIONSHIP_AND_DESCRIPTIONS": """
            Generate {n} text ads of less than {length} characters for Google Ads.
            The ad must be related to the terms '{term}' and '{associative_term}'.
            The text ad must encourage potential customers to buy '{term}' because '{associative_term}' is trending.

            The reponse should be in the following format:
            ["text 1 here", "text 2 here", ..., "text {n} here"]
            The response should be exactly in the provided format, without including line breaks or unnecessary spaces.
            It should only be a list of text ads separated by commas and between brackets.
          """,
            "WITHOUT_DESCRIPTIONS": """
            Generate {n} text ads of less than {length} characters for Google Ads.
            The ad must be related to the terms '{term}' and '{associative_term}'.
            The text ad must encourage potential customers to buy '{term}' because '{associative_term}' is trending.
            Consider the following association reason between both terms to create the ad: '{association_reason}'.
            If the generated text ads are long, try to include the retailer name: '{company}'.

            The response should be in the following format:
            ["text 1 here", "text 2 here", ..., "text {n} here"]
            The response should be exactly in the provided format, without including line breaks or unnecessary spaces.
            It should only be a list of text ads separated by commas and between brackets.
          """,
            "WITH_TERM_DESCRIPTION": """
            Generate {n} text ads of less than {length} characters for Google Ads.
            The ad must be related to the terms '{term}' whose description is '{term_description}' and '{associative_term}'.
            The text ad must encourage potential customers to buy '{term}' because '{associative_term}' is trending.
            Consider the following association reason between both terms to create the ad: '{association_reason}'.
            If the generated text ads are long, try to include the retailer name: '{company}'.

            The response should be in the following format:
            ["text 1 here", "text 2 here", ..., "text {n} here"]
            The response should be exactly in the provided format, without including line breaks or unnecessary spaces.
            It should only be a list of text ads separated by commas and between brackets.
          """,
            "WITH_ASSOCIATIVE_TERM_DESCRIPTION": """
            Generate {n} text ads of less than {length} characters for Google Ads.
            The ad must be related to the terms '{term}' and '{associative_term}' whose description is '{associative_term_description}'.
            The text ad must encourage potential customers to buy '{term}' because '{associative_term}' is trending.
            Consider the following association reason between both terms to create the ad: '{association_reason}'.
            If the generated text ads are long, try to include the retailer name: '{company}'.

            The response should be in the following format:
            ["text 1 here", "text 2 here", ..., "text {n} here"]
            The response should be exactly in the provided format, without including line breaks or unnecessary spaces.
            It should only be a list of text ads separated by commas and between brackets.
          """,
            "WITH_BOTH_DESCRIPTIONS": """
            Generate {n} text ads of less than {length} characters for Google Ads.
            The ad must be related to the terms '{term}' whose description is '{term_description}' and '{associative_term}' whose description is '{associative_term_description}'.
            The text ad must encourage potential customers to buy '{term}' because '{associative_term}' is trending.
            Consider the following association reason between both terms to create the ad: '{association_reason}'.
            If the generated text ads are long, try to include the retailer name: '{company}'.

            The response should be in the following format:
            ["text 1 here", "text 2 here", ..., "text {n} here"]
            The response should be exactly in the provided format, without including line breaks or unnecessary spaces.
            It should only be a list of text ads separated by commas and between brackets.
          """,
        },
        "WITHOUT_ASSOCIATIVE_TERM": {
            "WITH_DESCRIPTION": """
            Generate {n} text ads of less than {length} characters for Google Ads.
            The ad has to be related to the term '{term}' whose description is '{term_description}'.
            It is from a retailer called {company} and must encourage potential customers to buy '{term}'.
            If the generated text ads are long, try to include the retailer name: '{company}'.

            The response should be in the following format:
            ["text 1 here", "text 2 here", ..., "text {n} here"]
            The response should be exactly in the provided format, without including line breaks or unnecessary spaces.
            It should only be a list of text ads separated by commas and between brackets.
          """,
            "WITHOUT_DESCRIPTION": """
            Generate {n} text ads of less than {length} characters for Google Ads.
            The ad has to be related to the term '{term}'.
            It is from a retailer called {company} and must encourage potential customers to buy '{term}'.
            If the generated text ads are long, try to include the retailer name: '{company}'.

            The response should be in the following format:
            ["text 1 here", "text 2 here", ..., "text {n} here"]
            The response should be exactly in the provided format, without including line breaks or unnecessary spaces.
            It should only be a list of text ads separated by commas and between brackets.
          """,
        },
        "PATHS_WITHOUT_TERM_DESCRIPTION": """
        You will be provided with a term, and you should generate a url path split into {n} parts for that term.
        The path should refer to the term '{term}'.
        Each part of the path should be extremely short, just one word that encompasses the main idea of '{term}'
        and that takes into account the description '{term_description}'.

        For example, if the term is 'cell phones' and its description is 'Samsung Galaxy S23, Samsung Galaxy S23 Plus, Samsung Galaxy S23 Ultra',
        then part 1 of the path can be 'cell phones' and part 2 of the path can be 'galaxy-s23'.
        This path will be used in the url of an ecommerce site so that it will be displayed as follows: www.ecommerce.com/PATH1/PATH2.
        Example: www.ecommerce.com/cell-phones/galaxy-s23
        The first part of the path should be a category, for example 'cell phones', and the second part should be something more granular
        referring to the product, for example 'galaxy-s23'.
        These are some examples of PATHs with 2 parts: 'sneakers/nike-running', 'televisions/samsung', 'vehicles/ford-ranger'.
        IMPORTANT: It should NOT contain capital letters or spaces, if there are several words they should be in lowercase and separated by a hyphen.

        The response should be in the following format:
        ["path part 1 here", "path part 2 here", ..., "path part {n} here"]
        The response should be exactly in the provided format, without including line breaks or unnecessary spaces.
        It should only be a list of text ads separated by commas and between brackets.
      """,
        "PATHS_WITH_TERM_DESCRIPTION": """
        You will be provided with a term and its description, and you should generate a url path split into {n} parts for that term.
        The path should refer to the term '{term}' and its description '{term_description}'.
        Each part of the path should be extremely short, just one word that encompasses the main idea of '{term}'
        and that takes into account the description '{term_description}'.

        For example, if the term is 'cell phones' and its description is 'Samsung Galaxy S23, Samsung Galaxy S23 Plus, Samsung Galaxy S23 Ultra',
        then part 1 of the path can be 'cell phones' and part 2 of the path can be 'galaxy-s23'.
        This path will be used in the url of an ecommerce site so that it will be displayed as follows: www.ecommerce.com/PATH1/PATH2.
        Example: www.ecommerce.com/cell-phones/galaxy-s23
        The first part of the path should be a category, for example 'cell phones', and the second part should be something more granular
        referring to the product, for example 'galaxy-s23'.
        These are some examples of PATHs with 2 parts: 'sneakers/nike-running', 'televisions/samsung', 'vehicles/ford-ranger'.
        IMPORTANT: It should NOT contain capital letters or spaces, if there are several words they should be in lowercase and separated by a hyphen.

        The response should be in the following format:
        ["path part 1 here", "path part 2 here", ..., "path part {n} here"]
        The response should be exactly in the provided format, without including line breaks or unnecessary spaces.
        It should only be a list of text ads separated by commas and between brackets.
      """,
    },
    "SIZE_ENFORCEMENT": """
    Make the following text ad shorter, it has to be shorter than {max_length} characters.
    The text ad is: {copy}

    The response should be in the following format:
    shortened_text
    The response should be just the shortened text without quotation marks, line breaks or anything else.
  """,
    "PATH_SIZE_ENFORCEMENT": """
    I will give you a list of Responsive Search Ads display path texts for Google Ads that may be too long,
    from a list of paths, each individually called a part.  The path should be in the format of
    ["part 1 of the path", "part 2 of the path"], and it is possible for only one part to exist or
    the path being empty (which are valid cases).
    Check each part.  Make the part shorter if the part is greater than {max_length} characters, and check all parts.
    If a part does not need shortening, then keep the same part on the list.
    The text is: {copy}
    Give me the result in the following format (the same format as the text):
    ["write part 1 of the path here", "write part 2 of the path here"]
    The answer must be given to me exactly in the format that I have given you, without adding
    unnecessary line breaks or spaces. It should only be a list of texts separated by commas,
    everything between brackets and nothing else.
    IMPORTANT: It should NOT contain capital letters or spaces, if there are several words they should
    be in lowercase and separated by a hyphen.
  """,
    "EXTRACT_MAIN_FEATURES": """
    Given the following product description:
    '{description}'
    Generate a short list of the main features. The result should be in the following format:
    "Feature 1", "Feature 2", ..., "Feature N"
  """,
    "KEYWORDS_GENERATION": """
    Given the term '{term}', give me a list of up to 10 keywords for Google Ads that are related to the provided term.
    The response should be in the following format:
    ["Feature 1", "Feature 2", ..., "Feature N"]
    The response should be exactly in the provided format without adding unnecessary line breaks or spaces.
    It should only be a list of keywords separated by commas and between brackets.
  """,
}
