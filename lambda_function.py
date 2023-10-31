import base64
from urllib import parse
from modules.texting import handle_text


def lambda_handler(event, _):
    params = base64.b64decode(event["body"]).decode()

    requestDict = dict(parse.parse_qs(params))

    message = requestDict["Body"][0]
    number = requestDict["From"][0]

    handle_text(number, message)
    return
