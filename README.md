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

This program automates various tasks related to Google Ads campaigns and trends generation. It utilizes the Google Ads API, Google Sheets, BigQuery, and other services to streamline keyword management, trend analysis, and data integration.

Features:
1. Headlines, descriptions and keywords generation given a list of products or brands and (optionally) their descriptions.
2. Headlines, descriptions and keywords generation given a list of products or brands and trends if there is a relationship between them (meaning if the product or brand is trendy).
3. Data integration with Google Sheets.
4. Data integration with BigQuery.
5. Data integration with Merchant Center via BigQuery.
6. Data integration with Search Scout via BigQuery.
7. Data integration with Google Trends via BigQuery.
8. Data integration with RSS Feeds (pending).

##

Disclaimer: This is not an officially supported Google product.

## License

This program is licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0). See the [LICENSE](LICENSE) file for details.

© 2023 Google LLC

## Table of Contents

- [License](#license)
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Usage](#usage)
- [Features](#features)

## Introduction

This program is designed to help automate tasks related to Google Ads campaigns and trends analysis. It provides several functionalities, including keyword management, data integration with Google Sheets, and copies generation. It is licensed under the Apache License, Version 2.0.

## Prerequisites

Have a Google Cloud Platform project with a billing account and the following GCP APIs enabled:

1. Generative Language API
2. Google Ads API
3. Google Sheets API
4. BigQuery API

## Getting Started

Before using this program, you will need to configure it with your specific credentials and settings. Here are the initial steps:

1. Clone the repository to your local machine.
2. Set up `config.json` file
3. Run `deploy.sh` script
4. Share the spreadsheet(s) that are going to be used with the newly-created service account with edit permission (more details below)

## Configuration

The `config.json` file contains important settings and credentials required for the program to function. You must duplicate the file `config.json.example`, rename it to `config.json` and then edit this file to include your specific information. Here is an example of the `config.json` file:

```json
{
    "advertiser": "Company or brand name.",
    "project_id": "Google Cloud Platform proyect id to deploy Topic Mine.",
    "project_region": "Google Cloud Platform proyect id to retrieve data from - e.g.: us-central1.",
    "client_id": "Your client id - see Authentication params below.",
    "client_secret": "Your client secret - see Authentication params below.",
    "refresh_token": "Your refresh token - see Authentication params below.",
    "login_customer_id": "Your Google Ads customer id - see Authentication params below.",
    "google_ads_developer_token": "Your Google Ads developer token - see Authentication params below.",
    "gemini_api_token": "Your Gemini API token - see Authentication params below.",
    "cloud_run_service": "Cloud run service name to be created, e.g: topic-mine.",
    "service_account_name": "GCP service account name to be created, e.g: topic-mine-service-account.",
    "language": "Language to generate content. Supported values: ES, EN, PT.",
    "country": "Country for which the ads are for. E.g.: Mexico.",
}
```

### Authentication params

client_id and client_secret: Google Cloud console -> APIs & Services -> Credentials -> + Create credentials -> OAuth Client ID -> Desktop app

refresh_token:
1. Download credentials file generated in previous step
2. Rename it `creds.json` and paste inside `refresh_token_generator` folder
3. Run `refresh_token_generator.py`
4. Open url shown in terminal and follow steps
5. Once allowed permission, a site unreachable will appear in the web browser. Do not close it, copy the full url from the browser
6. Paste url in terminal and hit enter
7. Refresh token will be provided

login_customer_id: Usually at the top right of Google Ads console with a format similar to XXX-XXX-XXXX. Copy without dashes or hyphens.

google_ads_developer_token: Follow instructions [here](https://developers.google.com/google-ads/api/docs/get-started/dev-token)

gemini_api_token: Follow instructions [here](https://aistudio.google.com/app/apikey)

### [Optional] Prompts configuration

In the `/prompts/examples` directory, there are example prompt files. By default, Topic Mine will behave as if you are a retailer, so retailer-oriented prompts will be used. This can be changed by using one of the prompt files from the provided examples, or creating one of your own.

**Example**: If you are a university, you might want to copy the file `/prompts/examples/prompts_es.py.universities`, paste it and rename to `/prompts/prompts_es.py` (note the directory change from `/prompts/examples` to `/prompts`)

**Note**: If you want to use custom prompts you can do it, but beware that the return format must be explicitly and clearly specified in them.
**Note 2**: To add additional information to the prompts (for example, custom info related to the products), you can adapt the prompts accordingly and then you will need to adapt the part of the code that uses the prompts. That code is located in `/services/content_generator_service.py`, in the method called `__get_copy_generation_prompt`.


## Deployment

To deploy project, first set up the `config.json` file and then run the `deploy.sh` script.
**Important note:** once the project is deployed, share the spreadsheet(s) that are going to be used with the newly-created service account with edit permission.

### [Optional] Create a recurring job with Cloud Scheduler

Once deployed, you can create a job with Cloud Scheduler to run Topic Mine periodically. Steps:

1. Go to Cloud Scheduler and create new job.
2. In "Define the schedule": set name, frequency and timezone.
3. In "Configure the execution":
- **Target type**: HTTP
- **URL**: The one printed when running the `deploy.sh` script (can also be found in the new Cloud Run service) followed by de endpoint you want to use (e.g.: `https://topic-mine-xxx.a.run.app/content?...`)
- **HTTP method**: POST
- **HTTP headers**: The one that says "Content-Type" must have value "application/json" (if it doesn't show up, save the job and open edit mode again)
- **Body**: The body of the request (see details below)
- **Auth header**: Add OIDC token
- Service account:** The one created when deploying Topic Mine (set in file `config.json`)
- **Audience**: Same URL as before but without the endpoint resource (e.g.: `https://topic-mine-xxx.a.run.app/`)
4. In "Configure optional settings": set the attempt deadline to something longer (e.g.: 30m) so that the job does not fail when Topic Mine is still running


## Usage

This program exposes the following endpoints that you can access via HTTP requests:

### `/content`

- Description: Generates content based on client trends data.
- Method: POST

#### Query params

| Parameter              | Required                    | Description                                | Allowed Values                       |
|------------------------|-----------------------------|--------------------------------------------|--------------------------------------|
| `destination`          | Yes                         | Output format                              | `dv360feed`, `sa360feed`, `acsfeed`  |
| `first-term`           | Yes                         | First term (product/brand/services) source | `spreadsheet`, `big_query`           |
| `second-term`          | No                          | Second term (trends) source | `spreadsheet`,`google_trends`, `search_scout`, None |
|`must-find-relationship`| If `second-term` is present | Required if `second-term` is present       | `true`, `false`                      |


#### Body params

| Parameter                       | Required | Type      | Description                                                                         |
|---------------------------------|----------|-----------|-------------------------------------------------------------------------------------|
| `num_headlines`                 | Yes      | int       | Number of headlines to generate                                                     |
| `num_descriptions`              | Yes      | int       | Number of descriptions to generate                                                  |
| `first_term_source_config`      | Yes      | object    | Configuration for the first term source. See details below                          |
| `second_term_source_config`     | If `second-term` is present in query params | object | Configuration for the second term source. See details below |
| `destination_config`            | Yes      | object    | Configuration for the output destination. See details below                         |
| `headlines_blacklist`           | No       | list(str) | List of case-insensitive words or phrases that are blacklisted. Topic Mine will not generate headlines with these words or phrases. |
| `headlines_regexp_blacklist`    | No       | list(str) | List of regular expressions that are blacklisted. Topic Mine will not generate headlines that match with these regular expressions. Example: if descriptions with exclamation signs want to be avoided, use the regex '.*!'. Regular expression matching can be tested [here](https://regex101.com/). |
| `descriptions_blacklist`        | No       | list(str) | List of case-insensitive words or phrases that are blacklisted. Topic Mine will not generate headlines with these words or phrases. |
| `descriptions_regexp_blacklist` | No       | list(str) | List of regular expressions that are blacklisted. Topic Mine will not generate descriptions that match with these regular expressions. Example: if descriptions with exclamation signs want to be avoided, use the regex '.*!'. Regular expression matching can be tested [here](https://regex101.com/). |
| `generic_copies`                | No       | object    | Object with generic copies to be used if Gemini could not generate enough copies.  |
| `generic_copies.headlines`      | No       | list(str) | List of generic headlines.                                                         |
| `generic_copies.descriptions`   | No       | list(str) | List of generic descriptions.                                                      |
| `enable_feature_extraction`     | No       | bool      | If true, Topic Mine will understand the products' descriptions and extract their main features to generate the content. If false or not present, it will use the products' descriptions as they are. Good to try both cases and see what works best for you. |

##### first_term_source_config values if  `first-term` = `spreadsheet`

| Parameter                 | Required | Type   | Description                             |
|---------------------------|----------|--------|-----------------------------------------------------------------------|
| `spreadsheet_id`          | Yes      | string | Spreadsheet id to retrieve first term from                            |
| `sheet_name`              | Yes      | string | Worksheet name to retrieve first term from                            |
| `starting_row`            | Yes      | string | Row from which to start retrieving first term                         |
| `term_column`             | Yes      | string | Letter of the colum that contains the terms. E.g.: "A"                |
| `term_description_column` | No       | string | Letter of the colum that contains the terms' descriptions. E.g.: "B"  |
| `sku_column`              | No       | string | Letter of the colum that contains the skus. E.g.: "C"                 |
| `url_column`              | No       | string | Letter of the colum that contains the products' urls. E.g.: "D"       |
| `image_url_column`        | No       | string | Letter of the colum that contains the products' image urls. E.g.: "E" |

##### first_term_source_config values if  `first-term` = `big_query`

| Parameter                 | Required | Type   | Description                                            |
|---------------------------|----------|--------|--------------------------------------------------------|
| `query`                   | No*      | string | Query to run on BigQuery to obtain the first term. The query must return a table with the following column names: `term` (required), `term_description` (optional), `sku` (optional), `url` (optional), `image_url` (optional) |
| `project_id`              | Yes*     | string | Project id to run the query on                         |
| `dataset`                 | Yes*     | string | Dataset to run the query on                            |
| `table`                   | Yes*     | string | Table to run the query on                              |
| `term_column`             | Yes*     | string | Term column in the table                               |
| `term_description_column` | No       | string | Term description column in the table                   |
| `sku_column`              | No       | string | SKU column in the table                                |
| `url_column`              | No       | string | URL column in the table                                |
| `image_url_column`        | No       | string | Image URL column in the table                          |
| `limit`                   | Yes*     | int    | Max number of terms to fetch. limit = 0 means no limit |

* *Note: if query is present, all other params are ignored and are not required.

##### second_term_source_config values if  `second-term` = `google_trends`

| Parameter | Required | Type | Description                                             |
|-----------|----------|------|---------------------------------------------------------|
| `limit`   | Yes      | int  | Max number of trends to fetch. limit = 0 means no limit |

##### second_term_source_config values if  `second-term` = `search_scout`

| Parameter                 | Required | Type   | Description                                            |
|---------------------------|----------|--------|--------------------------------------------------------|
| `project_id`              | Yes      | string | Project id to run the query on                         |
| `dataset`                 | Yes      | string | Dataset to run the query on                            |
| `table`                   | Yes      | string | Table to run the query on                              |
| `term_column`             | Yes      | string | Term column in the table                               |
| `term_description_column` | No       | string | Term description column in the table                   |
| `min_label_weight`        | No       | double | Min label weight to retrieve data                      |
| `limit`                   | Yes      | int    | Max number of terms to fetch. limit = 0 means no limit |

##### second_term_source_config values if  `second-term` = `spreadsheet`

| Parameter                 | Required | Type   | Description                                                           |
|---------------------------|----------|--------|-----------------------------------------------------------------------|
| `spreadsheet_id`          | Yes      | string | Spreadsheet id to retrieve first term from                            |
| `sheet_name`              | Yes      | string | Worksheet name to retrieve first term from                            |
| `starting_row`            | Yes      | string | Row from which to start retrieving first term                         |
| `term_column`             | Yes      | string | Letter of the colum that contains the trends. E.g.: "A"               |
| `term_description_column` | No       | string | Letter of the colum that contains the trends' descriptions. E.g.: "B" |

##### destination_config required values if `destination` = `dv360feed` or `destination` = `sa360feed`

| Parameter                 | Required | Type   | Description                       |
|---------------------------|----------|--------|-----------------------------------|
| `spreadsheet_id`          | Yes      | string | Spreadsheet id to write output to |
| `sheet_name`              | Yes      | string | Worksheet name to write output to |

##### destination_config required values if `destination` = `acsfeed`

| Parameter             | Required | Type   | Description                                                                                    |
|-----------------------|----------|--------|------------------------------------------------------------------------------------------------|
| `spreadsheet_id`      | Yes      | string | Spreadsheet id to write output to                                                              |
| `sheet_name`          | Yes      | string | Worksheet name to write output to                                                              |
| `variant_name_column` | Yes      | string | Column that will contain the variant name for ACS. E.g.: "A"                                   |
| `constant_columns`    | Yes      | string | Columns that will remain constant (values will be copied from the row above). E.g.: ["B", "C"] |
| `copies_columns`      | Yes      | string | Columns that will contain the copies. E.g.: ["D", "E"]                                         |
| `starting_row`        | Yes      | string | Row from which to start writing output                                                         |

#### Request examples:

- POST `/content?destination=dv360feed&first-term-source=spreadsheet&second-term-source=google_trends&must-find-relationship=true`
```json
{
    "num_headlines": 10,
    "num_descriptions": 10,
    "first_term_source_config" : {
        "spreadsheet_id": "My products spreadsheet id",
        "sheet_name": "My products sheet name",
        "starting_row": 2,
        "term_column": "A",
        "term_description_column": "B"
    },
    "second_term_source_config" : {
        "limit": 10
    },
    "destination_config" : {
        "spreadsheet_id": "My output spreadsheet id",
        "sheet_name": "My output sheet name"
    },
    "headlines_blacklist": [
      "Unisex",
      "Cheap",
      "Free"
    ],
    "descriptions_blacklist": [
      "Get free",
    ]
}
```
- POST `/content?destination=acsfeed&first-term-source=big_query&second-term-source=search_scout&must-find-relationship=true`
```json
{
    "num_headlines": 5,
    "num_descriptions": 5,
    "first_term_source_config" : {
        "project_id": "My project id",
        "dataset": "My dataset",
        "table": "My table",
        "term_column": "product_title",
        "term_description_column": "product_description",
        "limit": 10
    },
    "second_term_source_config" : {
        "project_id": "My project id",
        "dataset": "My dataset",
        "table": "My table",
        "term_column": "product_title",
        "limit": 10
    },
    "destination_config" : {
        "spreadsheet_id": "My output spreadsheet id",
        "sheet_name": "My output sheet name",
        "variant_name_column": "B",
        "constant_columns": ["E"],
        "copies_columns": ["C", "D"],
        "starting_row": 2
    },
    "headlines_regexp_blacklist": [
      "[AZ]+"
    ]
}
```
- POST `/content?destination=sa360feed&first-term-source=big_query`
```json
{
    "num_headlines" : 3,
    "num_descriptions" : 3,
    "first_term_source_config" : {
        "query": "SELECT title AS term, description, product_id AS sku FROM `project.dataset.table` SORT BY title DESC LIMIT 10"
    },
    "destination_config" : {
        "spreadsheet_id": "My output spreadsheet id",
        "sheet_name": "My output sheet name"
    }
}
```

Please refer to the code for detailed functionality and usage.

#### Response examples:

HTTP code 202 Accepted:
```json
{
    "status": "accepted",
    "task_id": 2
}
```

HTTP code 409 CONFLICT:
```json
{
    "error": "Task already running"
}
```

HTTP code 400 BAD REQUEST:
```json
{
    "error": "Error message"
}
```

HTTP code 500 INTERNAL SERVER ERROR:
```json
{
    "error": "Error message"
}
```

### `/tasks/<task_id>`

- Description: Gets the status for a specific task id.
- Method: GET

#### Return examples:

HTTP code 200 OK:
```json
{
    "result": "completed",
    "status": "Task status (success/error)"
}
```

HTTP code 202 Accepted:
```json
{
    "status": "running"
}
```

HTTP code 404 NOT FOUND:
```json
{
    "error": "Task not found"
}
```

## Features

- Headlines, descriptions and keywords generation.
- Merchant Center and BigQuery integration to retireve products to generate ads of.
- Google Trends analysis and association with products/brands.
- Customizable configuration through `config.json`.


