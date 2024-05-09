<!--
 Copyright 2023 Google LLC

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 -->

# Topic Mine

Topic Mine leverages 1st and/or 2nd party data to identify trending topics and uses our GEMINI to create relevant ads' texts. It generates headlines, descriptions and keywords given a list of products, brands or services and (optionally) additional info about them.

### The solution has two options for operating

1. Internal trends: if the client identifies trending topics on their own (e.g.: trending products being purchased on their site, top search terms this week, etc.), Topic Mine takes these trending topics and generate ads' content for them. Clients usually identify trends with Google Analytics (GA4) data on their site. In this case, the input is literally a list of terms and [optionally] their descriptions or extra info about them.

2. External trends: if the client has a fixed list of products, brands or services they want to advertice (might be, for example, a category of products in particular), Topic Mine will take that list and try to find a relationship between each item and trending topics obtained from an external source. If there is a relationship between what the client offers and some trending topic, it will create ads' content for that.

### Benefits

- Always stay relevant to what is trending at the moment
- Generate ad content in bulk, saving lots of time in the creative process (clients say it takes 10x less time to do the same tasks)
- Obtain creative ideas for your ads
- Significantly reduce campaign production time
- Increased ROAS (about 4:1)
- Super cheap (between 2-4 USD / month if running once per week)
- Super easy to install

### Docs

Technical documentation and detailed instructions on how to configure and deploy can be found [here](https://github.com/google-marketing-solutions/topic-mine/wiki).