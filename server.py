from flask import Flask, request
from modules.texting import handle_text

app = Flask(__name__)


@app.route("/sms", methods=["GET", "POST"])
def sms_reply():
    message = request.values.get("Body", None)
    number = request.values.get("From", None)

    print("{}: {}".format(number, message))

    handle_text(number, message)
    return ""


if __name__ == "__main__":
    app.run(debug=True)
