import os
from flask import Flask, request, render_template
from imageasylib.utils import getSaAcessToken, get_iap_user, getSignedUrlParam

print("(RE)LOADING APPLICATION")
TOKEN = os.environ.get("TOKEN", "TOKEN")
print(f"TOKEN: {TOKEN}")
ANAMNEASY_ENDPOINT_API  = os.environ.get("ANAMNEASY_ENDPOINT_API", "http://127.0.0.1:8080")
print(f"ANAMNEASY_ENDPOINT_API: {ANAMNEASY_ENDPOINT_API}")
ANAMNEASY_TELE_ENDPOINT_API = os.environ.get("ANAMNEASY_TELE_ENDPOINT_API", "http://127.0.0.1:8080")
print(f"ANAMNEASY_TELE_ENDPOINT_API: {ANAMNEASY_TELE_ENDPOINT_API}")
DOCUMENT_ENDPOINT_API = os.environ.get("DOCUMENT_ENDPOINT_API", "http://127.0.0.1:8080")
print(f"DOCUMENT_ENDPOINT_API: {DOCUMENT_ENDPOINT_API}")


app = Flask(__name__)
timezone = None

def get_user_version_info():
    return "User: " + get_iap_user() + " -  Version: 1.0.1"

@app.route("/getAuthToken", methods=["GET"])
def getSignedUrl():
    print("METHOD: getSignedUrl")

    return getSaAcessToken()


@app.route("/", methods=["GET", "POST"])
def index():
    print("METHOD: index -> " + request.method)
    #if request.method == "POST":
    #    proceedWitForm()
    return renderIndex()

def renderIndex(page="index.html"):
    print("METHOD: renderIndex -> ")
    return render_template(page,
                           user_version_info=get_user_version_info(),
                           token=TOKEN,
                           anamneasy_api=ANAMNEASY_ENDPOINT_API,
                           anamneasy_tele_api=ANAMNEASY_TELE_ENDPOINT_API,
                           document_api=DOCUMENT_ENDPOINT_API)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
