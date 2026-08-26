One option is to us serverless approach to perform prediction on demand, instead fo having an EC2 server that runs continuously. Below are the steps to implement this option:

Here we will modify the model because the one we had has dependencies that make the lambda layer too big to fit the requirements, i.e., lambda layers cannot exceed 90MB (compressed) and 250MB (uncompressed). scikit-learn based models like ours will hit that ceiling very quickly. We have another option to deploy that (i.e., containers) -- we will come to that soon.

Now we will rewrite the code that builds the model and reduce dependencies.

## Step 1. Create an S3 Bucket

## Step 2. Build the model and upload it to the S3 Bucket
Use `end-to-end-regression-lambda.ipynb` to build the model and upload it to S3. Note that this Notebook uses the `model.py` file and you need to get it too.

## Step 3. Create the lambda layer
create a directory (e.g., python) and run the following:

`pip install -r requirements.txt -t python`. Note the `-t` which makes sure that the dependencies are downloaded to python folder.

`zip -r joblib-layer.zip python/`

## Step 4. Create Lambda Function
- Create lambda function and replace the default code with the code in `predict.py`
- Upload the `joblib-layer.zip` layer
- Upload `model.py`
- Add environment varialbes with their corresponding values, e.g., 
```
MODEL_BUCKET = "my-ml-bucket-2108"
MODEL_KEY = "model/exam_score_model.joblib"
```

## Step 4. Create API Gateway and Integration with Lambda
