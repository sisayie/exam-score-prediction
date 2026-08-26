# Create the client app, run it and perform prediction
from flask import Flask, request, jsonify
import joblib

import boto3

app = Flask(__name__)

## download the model from S3

BUCKET = "my-ml-bucket-2108"
MODEL_KEY = "model/exam_model.joblib"

s3 = boto3.client("s3")

s3.download_file(
	BUCKET,
	MODEL_KEY,
	"exam_model.joblib"
)

model = joblib.load(
"exam_model.joblib"
)

@app.get("/")
def home():
	return "Welcome to Flask on EC2"

@app.get("/predict")
def predict():

	hours = float(
    		request.args.get("hours")
	)

	prediction = model.predict(
    		[[hours]]
	)[0]

	return jsonify({
    		"hours_studied": hours,
    		"predicted_score":
        	round(float(prediction), 2)
	})
