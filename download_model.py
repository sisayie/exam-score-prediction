## Code to download the model from S3

import boto3

BUCKET = "my-ml-bucket-2108"
MODEL_KEY = "model/exam_model.joblib"

s3 = boto3.client("s3")

s3.download_file(
BUCKET,
MODEL_KEY,
"exam_model.joblib"
)
