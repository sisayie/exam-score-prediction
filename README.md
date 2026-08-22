# Practical Session on Using CloudFormation, Machine Learning model development and deployment on AWS Cloud

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

# Step 3. Create Key Pair
After you configure the credentials, run the following command to generate the key pair on your local machine.
`aws ec2 create-key-pair   --key-name exam-score-server-key   --query 'KeyMaterial'   --output text > exam-score-server.pem`

Then set its permission using `chmod 400 exam-score-server.pem`

If you are working on WSL, you need to move the key file to `~/.ssh`. Otherwise the permission setting won't take effect.

## Step 4. Setup the Infrastructure
After you create the key pair, you can run the following command to create the infrastructure, i.e., VPC, Subnet, EC2, Security Group, Internet Gateway, Route Table. 
4.1 Create the CloudFormation template

4.2 Get your public Ip

You can get your public IP using the command:
- in Linux 
	- `curl -4 ifconfig.me` or `curl -4 https://icanhazip.com` 
- In Windows, run:
	`(Invoke-RestMethod -Uri "https://api.ipify.org")`

4.3 Create the stack
```aws cloudformation create-stack 
--stack-name exam-score-server 
--template-body file://exam-score-ml-stack.yml 
--parameters 
   ParameterKey=KeyName,ParameterValue=exam-score-server-key
  ParameterKey=BucketName,ParameterValue=my-ml-bucket-2108
   ParameterKey=MyIp,ParameterValue=<your public ip>/32
```
The S3 bucket name needs to be globally unique. 

4.4 Verify the stack creation
Verify if the stack is created using:
`aws cloudformation describe-stacks --stack-name exam-score-server`

Or if you need more detailed information about the events,
`aws cloudformation describe-stack-events --stack-name exam-score-server`

You can also verify by using the AWS console: **CloudFormation** --> **Stacks**

In case you see the status correspoding to your stak name a value different from `CREATE_COMPLETE`, you can get more details about the events. You can see the events by clicking the stack name and opening the **Events* tab.
