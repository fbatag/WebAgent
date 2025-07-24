#!/bin/bash

# --- Configuration ---
# Please replace '[YOUR_PROJECT_ID]' with your actual GCP Project ID.
# The service account will be named 'search-engine-user'.
# The engine ID is taken from your request.
export PROJECT_ID=$(gcloud config get project)
export SA_NAME="sa-api-busca-cirurgias"
export SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
export ENGINE_ID="cirurgias_1745328426372"

# --- Step 1: Create a Service Account ---
echo "--- Creating Service Account: ${SA_NAME} ---"
if ! gcloud iam service-accounts describe "${SA_EMAIL}" --project="${PROJECT_ID}" &> /dev/null; then
  gcloud iam service-accounts create "${SA_NAME}" \
    --project="${PROJECT_ID}" \
    --display-name="Service Account for Specific Search Engine"
fi

echo "--- Verifying Service Account creation for ${SA_EMAIL} ---"
until gcloud iam service-accounts describe "${SA_EMAIL}" --project="${PROJECT_ID}" &> /dev/null; do
  echo "Waiting for service account to be created..."
  sleep 2
done
echo "--- Service Account ${SA_NAME} verified. ---"

# --- Step 2: Grant Conditional IAM Permission ---
# This command grants the 'Discovery Engine User' role to the service account,
# BUT only for resources under the specified engine ID.
echo "--- Granting conditional permission to ${SA_EMAIL} ---"
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/discoveryengine.user" \
  --condition="expression=resource.name.startsWith(\"projects/${PROJECT_ID}/locations/global/collections/default_collection/engines/${ENGINE_ID}/\"),title=engine_${ENGINE_ID}_access,description=Access to specific engine ${ENGINE_ID}"

echo "--- IAM Policy successfully updated. ---"


# --- Step 3: Create a Service Account Key ---
# This creates a JSON key file that your application can use to authenticate as the service account.
# This is NOT an API Key, but a more secure credential for server-to-server interaction.
echo "--- Creating a key for the service account ---"
gcloud iam service-accounts keys create "sa-key-for-${ENGINE_ID}.json" \
  --iam-account="${SA_EMAIL}"

echo "---"
echo "✅ All steps completed."
echo "Key file created: sa-key-for-${ENGINE_ID}.json"
echo "🔴 IMPORTANT: Secure this file. It provides access to your GCP resources."
