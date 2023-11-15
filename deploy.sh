#!/bin/bash
# Copyright 2022 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    https://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

echo "Setting variable values..."
project_id=$(cat config.json | jq -r '.deployment_project_id')
project_region=$(cat config.json | jq -r '.project_region')
cloud_run_service=$(cat config.json | jq -r '.cloud_run_service')
service_account_name=$(cat config.json | jq -r '.service_account_name')

echo "Enabling required API services..."
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable googleads.googleapis.com
gcloud services enable sheets.googleapis.com

echo "Setting Google Cloud project..."
gcloud config set project "$project_id"

echo "Creating Service Account..."
gcloud iam service-accounts create $service_account_name --display-name "BardTrender Service Account"
gcloud projects add-iam-policy-binding $project_id \
    --member serviceAccount:$service_account_name@$project_id.iam.gserviceaccount.com \
    --role roles/bigquery.admin

echo "Deploying Cloud Run..."
gcloud run deploy $cloud_run_service --region=$project_region --source="."

echo "Testing correct deployment..."
echo "url: $cloud_run_url"
echo "Authorization: Bearer $(gcloud auth print-identity-token)"
cloud_run_url=$(gcloud run services describe $cloud_run_service --platform managed --region $project_region --format 'value(status.url)')
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" "$cloud_run_url/test"