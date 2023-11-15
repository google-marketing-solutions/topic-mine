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

# Bardtrender

This program automates various tasks related to Google Ads campaigns and trends generation. It utilizes the Google Ads API, Google Sheets, BigQuery, and other services to streamline keyword management, trend analysis, and data integration.

So far, it has two running modes: Client trends and Google trends. In Client trends mode, it will generate ad copies and keywords given the trends the client has registered on their site. In Google trends mode, it will check the latest trends from Google Search, try to match them with the brands or products that the client sells, and then create ad copies and keywords for those that do match.

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

This program is designed to help automate tasks related to Google Ads campaigns and trends analysis. It provides several functionalities, including keyword management, data integration with Google Sheets, and trend generation. It is licensed under the Apache License, Version 2.0.

## Prerequisites

Have the following APIs enabled:

1. Vertex AI API
2. Google Ads API
3. Google Sheets API
4. Google Drive API
5. BigQuery API

## Getting Started

Before using this program, you will need to configure it with your specific credentials and settings. Here are the initial steps:

1. Clone the repository to your local machine.
2. Set up `config.json` file
3. Run `deploy.sh` script

## Configuration

The `config.json` file contains important settings and credentials required for the program to function. You must duplicate the file `config.json.example`, rename it to `config.json` and then edit this file to include your specific information. Here is an example of the `config.json` file:

```json
{
    "advertiser": /* Company or brand name */,
    "deployment_project_id": /* Google Cloud Platform proyect id to deploy Bardtrender */,
    "project_id": /* Google Cloud Platform proyect id to retrieve data from */,
    "project_region": /* Google Cloud Platform proyect region */, 
    "client_id": /* Your client id */,
    "client_secret": /* Your client secret */,
    "refresh_token": /* Your refresh token */,
    "login_customer_id": /* Your Google Ads customer id */, 
    "dev_token": /* Your Google Ads developer token */,
    "cloud_run_service": /* Cloud run service name to be created, e.g: "bardtrender" */,
    "service_account_name": /* GCP service account name to be created, e.g: "bardtrender-service-account" */ ,
    "low_performance_mode": /* Values accepted: true, false. If you get Vertex AI text-bison model quota error, set value true. This is to limit performance and not exceed Vertex AI text-bison model quota. */, 
    "language": /* Language to generate content. Supported values: "ES", "EN", "PT". */,
    "google_trends": {
        // ... (See google trends configuration below)
    },
    "client_trends": {
        // ... (See client trends configuration below)
    },
    "palm_examples":{
        "headlines": /* List of headline examples used for inspiration */,
        "descriptions": /* List of description examples used for inspiration */
    },

    "keywords": {
        // ... (See keywords configuration below)
    }
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

dev_token: Follow instructions [here](https://developers.google.com/google-ads/api/docs/access-levels)

### Google trends configuration

The `google_trends` section in the `config.json` file contains settings and parameters related to google trends analysis and generation. Below, we describe each component of this configuration:

```json
"google_trends" : {
        "big_query":{
            "trends_params": {
                "international": /* A boolean flag indicating whether the analysis is international. */,
                "country_name": /* The name of the country for trends analysis (e.g., "Mexico") */
            }
        },
        "google_sheets":{
            "spreadsheet_id": /* The unique identifier of the Google Sheets spreadsheet. */,
            "sheet_name": /* The name of the sheet. */
        },
        "brand_params": {
            "merchant_center": /* A boolean flag indicating whether Merchant Center data will be used. */,
            "merchant_center_table_name": /* The table name for Merchant Center data (if applicable). */,
            "brands": /* A list of brands to try to find relationship with trends. (e.g.: "[ "Nike", "Adidas", ... ]") */
        },
        "google_ads": {
            "num_headlines": /* The number of headlines to generate for Google Ads. For Search Ads recommended 5. For DV360 recommended 1. */,
            "num_descriptions": /* The number of descriptions to generate for Google Ads. For Search Ads recommended 1. For DV360 recommended 0. */,
        }
    },
```

### Client trends configuration

The `client_trends` section in the `config.json` file contains settings and parameters related to client trends analysis and generation. Below, we describe each component of this configuration:

```json
"client_trends":{
        "big_query":{
            "dataset": /* The BigQuery dataset used for retrieving client trends data. */,
            "current_state_table": /* Temporal table */,
            "trends_limit": /* Limit number of top trends results */,
        },
        "queries":{
            "trends": /* Query to be executed in BigQuery that must return a table with client trends data. Return format described below. */
        },
        "google_ads":{
            "num_headlines": /* The number of headlines to generate for Google Ads. For Search Ads recommended 5. For DV360 recommended 1. */,
            "num_descriptions": /* The number of descriptions to generate for Google Ads. For Search Ads recommended 1. For DV360 recommended 0. */,
            "trends_google_ads_path_one": /* The first part of the URL path for Google Ads campaigns. */,
            "search_bar_url": /* Site url path when search (e.g.: "https://www.yoursite.com/store?s={search_term}") */
        },
        "google_sheets":{
            "spreadsheet_id": /* The unique identifier of the Google Sheets spreadsheet. */,
            "sheet_name": /* The name of the sheet. */
        }
    },
```

#### trends query return table format

| search_term | title  | description | product_link | image_link | product_type | searches | sku    | views |
|-------------|--------|-------------|--------------|------------|--------------|----------|--------|-------|
| string      | string | string      | string       | string     | string       | int      | string | int   |

##### Required fields:

- search_term: Trending search term. Used to generate copies. Can be omitted if title is present. Will prioritize title if both present.
- title: Trending product title. Used to generate copies. Can be omitted if search_term is present. Will be prioritized if both present.
- product_link: Required for the Search Ads and DV360 feeds.
- image_link: Required for the DV360 feed. 

##### Optional fields to add more information to Bardtrender's output if needed:

- description
- product_type
- searches
- views
- sku
- product_category
- etc...

### Keywords configuration

The `keywords` section in the `config.json` file contains settings and parameters related to keywords generation. Below, we describe each component of this configuration:

```json
"keywords": {
        "language_code": /* Language to generate (e.g., "1003") */,
        "region_codes": /* List of region codes to be used obtained from https://developers.google.com/google-ads/api/data/geotargets (e.g., ["2484", ...])  */,
        "url": /* Incoming feature: url seed for keywords suggestion - can be empty for now (e.g., "https://www.yoursite.com/") */
    }
```
## Deployment

To deploy project, first set up the `config.json` file and then run the `deploy.sh` script.

### [Optional] Create a recurring job with Cloud Scheduler

Once deployed, you can create a job with Cloud Scheduler to run Bardtrender periodically. Steps:

First configure the service account to have permission to run the service:
1. Go to IAM & Admin -> IAM
2. Identify the service account created when deploying Bardtrender (set in file `config.json`) and click the edit button on the right
3. Add the role "Cloud Run Invoker" and save changes

Then create the job and use that service account:
1. Go to Cloud Scheduler and create new job. 
2. In "Define the schedule": set name, frequency and timezone.
3. In "Configure the execution":
- Target type: HTTP
- URL: The one printed when running the `deploy.sh` script (can also be found in the new Cloud Run service) followed by de endpoint you want to use (e.g.: `https://bardtrender-xxx.a.run.app/trends/client/generate`)
- HTTP method: GET
- Auth header: Add OIDC token
- Service account: The one created when deploying Bardtrender (set in file `config.json`)
- Audience: Same URL as before but without the endpoint resource (e.g.: `https://bardtrender-xxx.a.run.app/`)
4. In "Configure optional settings": set the attempt deadline to something longer (e.g.: 30m) so that the job does not fail when Bardtrender is still running


## Usage

This program exposes the following endpoints that you can access via HTTP requests:

### `/test`

- Description: A test endpoint that returns a "Hello world!" message.
- Method: GET

### `/trends/client/generate`

- Description: Generates content based on client trends data.
- Method: GET

#### Body params

- `start_date` (string): The starting date to retreive client trends data in the format "YYYY-MM-DD". Defaults to today.
- `end_date` (string): The ending date to retreive client trends data in the format "YYYY-MM-DD". Defaults to one week ago.

### `/trends/google/generate`

- Description: Generates content based on google trends data.
- Method: GET


Please refer to the code for detailed functionality and usage.

## Features

- Keyword management and automation.
- Integration with Google Ads and Google Sheets.
- Trend generation and analysis.
- Customizable configuration through `config.json`.


