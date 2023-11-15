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

import json
from typing import Any
from utils.vertex_ai_helper import VertexAIHelper
from prompts.prompts import prompts

class Utils:
    """
    This class contains multiple utilities
    """
    def load_config(config_file_name) -> Any:
        """Loads the configuration data from the given path.

        Args:
            config_file_name: The name of the configuration file to load.

        Returns:
            The contents of the configuration file as a JSON object.
        """
        config_file_path = './' + config_file_name
        with open(config_file_path, 'r') as config_file:
            return json.load(config_file)

    def enforce_text_size(config, copy:str, type:str, retries:int = 5) -> str:
        """
        Enforces size limits on generated content of a specified type.

        Parameters:
        - copy (str): The generated content to be checked and potentially resized.
        - type (str): The type of content ('headlines', 'descriptions', etc.) for which size limits apply.
        - retries (int, optional): The number of retry attempts for resizing content (default is 5).

        Returns:
        - str: The resized content that meets the size limits.
        """
        if type == 'headlines':
            max_length = 30
        elif type == 'descriptions':
            max_length = 90
        else:
            raise Exception(f"Unsupported value: {type}. Supported values are 'headlines' and 'descriptions'")

        if retries == 0:
            return "Review: " + copy
        else:
            prompt = Utils.__get_enforce_size_prompt(config, copy, type)

            vertex_helper = VertexAIHelper(config)
            result = vertex_helper.run_prompt(prompt)

            if(len(result) > max_length):
                return Utils.enforce_text_size(config, result, type, retries-1)
            else:
                return result
    
    def __get_enforce_size_prompt(config, copy: str, type: str) -> str:
        """
        Generates a text prompt enforcing copy sizes.

        Parameters:
        - copy (str): The copy that is too long.
        - type (str): The type (headlines|descriptions).

        Returns:
        - str: A text prompt for shortening the copy.
        """
        if type == 'headlines':
            max_length = 30
        elif type == 'descriptions':
            max_length = 90
        else:
            raise Exception(f"Unsupported value: {type}. Supported values are 'headlines' and 'descriptions'")

        return prompts[config['language']]['SIZE_ENFORCEMENT'].format(
                max_length=max_length,
                copy=copy,
            )
