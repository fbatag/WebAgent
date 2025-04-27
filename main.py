from flask import Flask, request, render_template
from imageasylib.utils import get_project_Id, get_iap_user, getSignedUrlParam


print("(RE)LOADING APPLICATION")

app = Flask(__name__)
timezone = None

def get_user_version_info():
    return "User: " + get_iap_user() + " -  Version: 1.0.0"

@app.route("/getSignedUrl", methods=["GET"])
def getSignedUrl():
    print("METHOD: getSignedUrl")
    print(request.args)
    dest_bucket_name = request.args.get("dest_bucket")
    dest_object = request.args.get("dest_object")
    filetype = request.args.get("filetype")
    return getSignedUrlParam(dest_bucket_name, dest_object, filetype)


@app.route("/", methods=["GET", "POST"])
def index():
    print("METHOD: index -> " + request.method)
    return renderIndex()

def renderIndex(page="index.html"):
    print("METHOD: renderIndex -> ")
    return render_template(page, user_version_info=get_user_version_info())

if __name__ == "__main__":
    app.run(debug=True)

