import json
import os 

import joblib
import boto3

from model import LinearRegression

BUCKET = os.environ["MODEL_BUCKET"]
MODEL_KEY = os.environ["MODEL_KEY"]

MODEL_PATH = "/tmp/exam_score_model.joblib"

s3 = boto3.client("s3")

s3.download_file(
    BUCKET,
    MODEL_KEY,
    MODEL_PATH
)

model = joblib.load(
    MODEL_PATH
)

def lambda_handler(event, context):
    print("EVENT:")
    print(json.dumps(event))

    params = event.get("queryStringParameters") or {}

    hours = params.get("hours")

    if hours is None:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Missing 'hours' parameter"
            })
        }

    hours = float(hours)

    prediction = model.predict([hours])[0]

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "hours": hours,
            "prediction": prediction
        })
    }
