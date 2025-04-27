from flask import Flask, request, render_template
from imageasylib.utils import get_project_Id, get_iap_user, getSignedUrlParam


print("(RE)LOADING APPLICATION")

app = Flask(__name__)
timezone = None

def get_user_version_info():
    return "User: " + get_iap_user() + " -  Version: 1.0.0"

@app.route("/getAuthToken", methods=["GET"])
def getSignedUrl():
    print("METHOD: getSignedUrl")

    return getSignedUrlParam(dest_bucket_name, dest_object, filetype)


@app.route("/", methods=["GET", "POST"])
def index():
    print("METHOD: index -> " + request.method)
    return renderIndex()

def renderIndex(page="index.html"):
    print("METHOD: renderIndex -> ")
    jwtoken = request.headers.get('X-Goog-Iap-Jwt-Assertion', "None")
    return render_template(page, user_version_info=get_user_version_info(), jwtoken=jwtoken)

if __name__ == "__main__":
    app.run(debug=True)

