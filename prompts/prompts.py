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

from prompts.prompts_es import prompts_es
from prompts.prompts_en import prompts_en
from prompts.prompts_pt import prompts_pt

prompts = {
    'ES': prompts_es,
    'EN': prompts_en,
    'PT': prompts_pt
}