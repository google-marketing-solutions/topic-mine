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
project_id=$(cat config.json | jq -r '.project_id')
project_region=$(cat config.json | jq -r '.project_region // "us-central1"')
cloud_run_service=$(cat config.json | jq -r '.cloud_run_service // "topic-mine"')
service_account_name=$(cat config.json | jq -r '.service_account_name // "topic-mine-service-account"')

echo "Setting Google Cloud project..."
gcloud config set project "$project_id"

enable_gcp_services() {
    echo "Enabling required API services..."
    gcloud services enable run.googleapis.com
    gcloud services enable artifactregistry.googleapis.com
    gcloud services enable cloudbuild.googleapis.com
    gcloud services enable aiplatform.googleapis.com
    gcloud services enable googleads.googleapis.com
    gcloud services enable sheets.googleapis.com
}


create_service_account_and_permissions() {
    echo "Creating Service Account..."
    gcloud iam service-accounts create $service_account_name --display-name "Topic Mine Service Account"
    gcloud projects add-iam-policy-binding $project_id \
        --member serviceAccount:$service_account_name@$project_id.iam.gserviceaccount.com \
        --role roles/bigquery.jobUser
    gcloud projects add-iam-policy-binding $project_id \
        --member serviceAccount:$service_account_name@$project_id.iam.gserviceaccount.com \
        --role roles/bigquery.dataViewer
    gcloud projects add-iam-policy-binding $project_id \
        --member serviceAccount:$service_account_name@$project_id.iam.gserviceaccount.com \
        --role roles/aiplatform.user
    gcloud projects add-iam-policy-binding $project_id \
        --member serviceAccount:$service_account_name@$project_id.iam.gserviceaccount.com \
        --role roles/run.invoker
}

# Deployment

enable_gcp_services

EXISTING_SERVICE_ACCOUNT=$(gcloud iam service-accounts list --filter "email:${service_account_name}" --format="value(email)")
echo $EXISTING_SERVICE_ACCOUNT

if [ -z "${EXISTING_SERVICE_ACCOUNT}" ]; then
    create_service_account_and_permissions
    echo
else
    echo
    echo "${text_yellow}INFO: Service account '${service_account_name}' already exists. ${reset}"
    echo "${text_yellow}INFO: Please check that the service account has all the required permissions to run the solution. ${reset}"
    echo
fi

echo "Deploying Cloud Run..."
gcloud run deploy $cloud_run_service --region=$project_region --source="." \
    --service-account $service_account_name \
    --timeout 3600 \
    --memory 4Gi
