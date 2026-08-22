# Practical Session on Using CloudFormation, Machine Learning model development and deployment on AWS Cloud

In this exercise, you will develop and deploy a simple linear regression model on AWS. The exercise enables you to practice the following key AWS services, S3, SageMaker, EC2, CloudFormation, VPC, Internet Gateway, Subnet, Security Group, Route Table and IAM. In addition, it provides a solid structure of ecosystem to develop a secure, scalable machine learning app.

## Step 1. Install Amazon CLI
```
apt update
apt install awscli
```

---

## Step 2. Configure Credentials
When prompted, enter the key and secret provided after you created the sandbox.

`aws configure`

AWS Access Key ID []: <the key in the sandbox>

AWS Secret Access Key []: <the secret in the sandbox>

Default region name []: 

Default output format []: 

---

## Step 3. Create Key Pair
After you configure the credentials, run the following command to generate the key pair on your local machine.
`aws ec2 create-key-pair   --key-name exam-score-server-key   --query 'KeyMaterial'   --output text > exam-score-server.pem`

Then set its permission using `chmod 400 exam-score-server.pem`

If you are working on WSL, you need to move the key file to `~/.ssh`. Otherwise the permission setting won't take effect.

## Step 4. Setup the Infrastructure
After you create the key pair, you can run the following command to create the infrastructure, i.e., VPC, Subnet, EC2, Security Group, Internet Gateway, Route Table. 
### 4.1 Create the CloudFormation template
You can download the [CloudFormation template file](exam-score-ml-stack.yml) included in this project. You may change it to suit your needs.
### 4.2 Get your public Ip

You can get your public IP using the command:
- in Linux 
	- `curl -4 ifconfig.me` or `curl -4 https://icanhazip.com` 
- In Windows, run:
	`(Invoke-RestMethod -Uri "https://api.ipify.org")`

### 4.3 Create the stack
```
aws cloudformation create-stack \
--stack-name exam-score-server \
--template-body file://exam-score-ml-stack.yml \
--parameters \
   ParameterKey=KeyName,ParameterValue=exam-score-server-key \
  ParameterKey=BucketName,ParameterValue=my-ml-bucket-2108 \
   ParameterKey=MyIp,ParameterValue=<your public ip>/32
```
The S3 bucket name needs to be globally unique. 

### 4.4 Verify the stack creation
Verify if the stack is created using:
`aws cloudformation describe-stacks --stack-name exam-score-server`

Or if you need more detailed information about the events,
`aws cloudformation describe-stack-events --stack-name exam-score-server`

You can also verify if the individual AWS services are created using the console.

You can also verify by using the AWS console: **CloudFormation** --> **Stacks**

In case you see the status correspoding to your stak name a value different from `CREATE_COMPLETE`, you can get more details about the events. You can see the events by clicking the stack name and opening the **Events** tab.

---

## 5. Build the Model
### 5.1 Upload data to S3 Bucket
Upload dataset to data folder of S3 bucket using `aws s3 cp <path-to-data> s3://<bucket-name>/<path-to-data>

Example:

```
aws s3 cp data/exam_scores.csv \
        s3://my-ml-bucket-2108/data/exam_scores.csv
```
### 5.2 Build and Deploy Model on SageMaker
Use the [Notepad] (exam-score-linear-regression-example.ipynb) to build the model and upload it to S3 on On SageMaker.
---

## 6. Setup the EC2 Server
### 6.1 Connect to the EC2 server via ssh
ssh -i ~/.ssh/exam-score-server.pem ubuntu@<public-ip-of-EC2-Instance>

### 6.2 Create python virtual environment. Install if you need to.
`sudo apt update`

`sudo apt install python3.12-venv`

`python3 -m venv .venv`

`source .venv/bin/activate`

### 6.3 Install required libraries
`pip install -r requirements.txt`

### 6.4 Perform Prediction 
Run [download_model.py]("download_model.py") with `python download_model.py` 

But before you run the file, you may need to first set the credentials.
    
```
# -- install awscli 
apt update
apt install awscli 
```

#if the above command does not work, use the following to install awscli
```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip -y
unzip awscliv2.zip
sudo ./aws/install
```
Then run the command in Step 2 above on the EC2 server

After credentials are in place, you can run `python download_model.py`

Then create the predict.py file on the EC2 server and run `flask --app predict run --host 0.0.0.0 --port 8000 &`. The `&` is needed to run the flask app in the background. By doing so, you cna run other commands on the same terminal. If you omit `&`, you may have to start another terminal, connect to EC2 via ssh and run the next command.

Finally, on 
curl "http://localhost:8000/predict?hours=8"

You should see, 
{"hours_studied":8.0,"predicted_score":74.88}

Congratulations! 
You have completed developing and deploying an end-to-end machine learning model on AWS!
