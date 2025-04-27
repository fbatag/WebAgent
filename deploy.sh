export PROJECT_ID=$(gcloud config get project)
echo $PROJECT_ID
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID | grep projectNumber | grep -Eo '[0-9]+')
echo $PROJECT_NUMBER
export REGION=southamerica-east1
export APP_NAME=webagent
export SERVICE_ACCOUNT=$APP_NAME-sa

gcloud services enable iam.googleapis.com
gcloud services enable storage-component.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable cloudbuild.googleapis.com # para o Cloud Run
gcloud services enable iap.googleapis.com 
gcloud services enable run.googleapis.com

gcloud iam service-accounts create $SERVICE_ACCOUNT \
--display-name "WebAgent Service Account" \
--project $PROJECT_ID

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com \
--role roles/aiplatform.user

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com \
--role roles/serviceusage.serviceUsageConsumer

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com \
--role roles/iam.serviceAccountTokenCreator

#deploy em Cloud Run (não é necessário yaml)
gcloud beta run deploy $APP_NAME --source . --region=$REGION \
   --service-account=$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com \
   --project=$PROJECT_ID --no-allow-unauthenticated --iap --min-instances=0  
   --verbosity=debug 
   --quiet

# Configurar o IAP para o LB *precisa ser rodado somente uma vez)
gcloud beta services identity create --service=iap.googleapis.com --project=$PROJECT_ID
gcloud run services add-iam-policy-binding $APP_NAME --member=serviceAccount:service-$PROJECT_NUMBER@gcp-sa-iap.iam.gserviceaccount.com  \
--role='roles/run.invoker' --region $REGION

# Usuário da aplicação = permissão no IAP    
gcloud beta iap web add-iam-policy-binding \
--member=user:dev@fbatagin.altostrat.com  \
--role=roles/iap.httpsResourceAccessor \
--region=$REGION \
--resource-type=cloud-run \
--service=$APP_NAME

#gcloud projects add-iam-policy-binding $PROJECT_ID --member=group:dev@fbatagin.altostrat.com --role=roles/iap.httpsResourceAccessor

#gcloud iap oauth-brands create --application_title=$APP_NAME --support_email=dev@fbatagin.altostrat.com
#gcloud iap oauth-clients create minha-empresa --display_name=$APP_NAME
#gcloud iap web enable --resource-type=backend-services --service=$APP_NAME
