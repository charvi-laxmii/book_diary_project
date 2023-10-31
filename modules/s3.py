from zoneinfo import ZoneInfo
import boto3

S3 = boto3.resource("s3")
MESSAGE_LOG_BUCKET = "book-diary-message-log"

from datetime import datetime


def writeToMessageLog(number: str, message: str, modifier: str) -> None:
    currentTime = str(datetime.now(tz=ZoneInfo("America/Chicago")))
    s3Object = S3.Object(MESSAGE_LOG_BUCKET, "{}/{}.txt".format(number, currentTime))
    s3Object.put(Body="{}: {}".format(modifier, message))
