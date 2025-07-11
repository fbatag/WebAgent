from flask import Flask, request, render_template
from imageasylib.utils import getSaAcessToken, get_iap_user, getSignedUrlParam


print("(RE)LOADING APPLICATION")

app = Flask(__name__)
timezone = None

def get_user_version_info():
    return "User: " + get_iap_user() + " -  Version: 1.0.0"

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
    #jwtoken = request.headers.get('X-Goog-Iap-Jwt-Assertion', "None") -> não funcionou ...
    return render_template(page, user_version_info=get_user_version_info())
    #return render_template(page, user_version_info=get_user_version_info(), jwtoken=getSaAcessToken())
   

if __name__ == "__main__":
    app.run(port=5000, debug=True)

