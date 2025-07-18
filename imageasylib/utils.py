import  os, datetime
from flask import request
from google import auth
from google.oauth2 import service_account
from google.cloud import storage

storage_client = storage.Client()
local_cred_file = os.environ.get("HOME") +"/.config/gcloud/imageasy_sa.json"

def getSaAcessToken():
    print("METHOD: getSaAcessToken")
    credentials, project_id = auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
    #credentials, project_id = auth.default()
    #if credentials.token is None:
    credentials.refresh(auth.transport.requests.Request())
    print("Using service account")
    print(credentials.service_account_email)
    print("TODO REMOVER _ TOKEN")
    print(credentials.token)
    try:
        print(credentials.expired)
    except Exception as e:
        print(e)
    return credentials.token


def get_project_Id():
    return storage_client.project

def get_iap_user():
    print("METHOD: get_iap_user")
    user = request.headers.get('X-Goog-Authenticated-User-Email', "None")
    if user != "None":
        user = user.replace("accounts.google.com:","")
    return user

def get_user_folder():
    print("METHOD: get_user_folder")
    user = get_iap_user()
    temp_user_dir = user.replace("@", "_").replace(".", "_")
    return temp_user_dir

def get_user_files(bucket_name):
    print("METHOD: get_user_files -> ")
    bucket = storage_client.bucket(bucket_name)
    return bucket.list_blobs(prefix=get_user_folder())

def getSignedUrlParam(dest_bucket_name, dest_object, filetype):
    dest_bucket = storage_client.bucket(dest_bucket_name)
    blob = dest_bucket.blob(dest_object)
    expiration=datetime.timedelta(minutes=15)

    print('Content-Type: '+  filetype)
    if request.url_root == 'http://127.0.0.1:5000/':
        print("RUNNING LOCAL")
        signeUrl = blob.generate_signed_url(method='PUT', version="v4", expiration=expiration, content_type=filetype, 
                                    credentials=service_account.Credentials.from_service_account_file(local_cred_file),
                                    headers={"X-Goog-Content-Length-Range": "1,5000000000", 'Content-Type': filetype})
    else:
        signeUrl = blob.generate_signed_url(method='PUT', version="v4", expiration=expiration, content_type=filetype, 
                                    service_account_email=credentials.service_account_email, access_token=getSaAcessToken(),
                                    headers={"X-Goog-Content-Length-Range": "1,5000000000", 'Content-Type': filetype})
        #except Exception as e:
        #    print(e)
    print(signeUrl)
    return signeUrl

