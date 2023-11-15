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
    'GOOGLE_TRENDS': {
        'FIND_RELATIONSHIP':  """
                              I want you to tell me if you find a clear relationship between two concepts I will give you.
                              The first one is {brand} and the second one is {trend}.

                              Response must be in JSON format, following this example:
                              {{"trend": "{trend}", "brand": "{brand}", "relationship": true/false, "reason": "reason why there is or isn't relationship between {brand} and {trend}"}}
                              """,
        'COPIES_GENERATION':    """
                                I want to generate {n} texts of less than {length} characters for a Google Ads ad.
                                This ad has to be related to a trending topic, in this case {trend}, and with the brand {brand}.
                                Consider that the reason why the brand and the trending topic are related is: {association_reason}.
                                It is extremely important that they are as short as possible, they must be shorter than {length} characters.
                                Try to include key words related with the trending topic in the texts.
                                If the generated texts are long, try to include the retailer's name, which is {company}, in the texts.

                                Here you have some examples that you can use as inspiration to create the new texts that you will give me:

                                {examples}

                                Make sure that the texts comply with the policies described here: https://support.google.com/adspolicy/answer/6008942?hl=en#con

                                Response must be in exactly the following format:
                                ["write here the text 1", "write here the text 2", ..., "write here the text {n}"]
                                The response must follow exactly that format. It does not have to contain any additional commas, whitespaces or line breaks. It must be just a comma-separated list of texts between square brackets and thats it.
                                """
    }, 
    'CLIENT_TRENDS': {
        'COPIES_GENERATION':    """
                                I want to generate {n} texts of less than {length} characters for a Google Ads ad.
                                This ad has to be related to a product, in this case {title}.
                                It is from a retailer called {company} and should invite the customer to buy because the product is somehow trendy.
                                It is extremely important that they are as short as possible, they must be shorter than {length} characters.
                                Try to include key words related with the product in the text.
                                If the generated texts are long, try to include the retailer's name, which is {company}, in the texts.

                                Here you have some examples that you can use as inspiration to create the new texts that you will give me:


                                {examples}

                                Make sure that the texts comply with the policies described here: https://support.google.com/adspolicy/answer/6008942?hl=en#con

                                Response must be in exactly the following format:
                                ["write here the text 1", "write here the text 2", ..., "write here the text {n}"]
                                The response must follow exactly that format. It does not have to contain any additional commas, whitespaces or line breaks. It must be just a comma-separated list of texts between square brackets and thats it.
                                """
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