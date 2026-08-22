# Create the client app, run it and perform prediction
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

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
