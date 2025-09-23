# End-to-End-Devops

## Overview
Github -> Jenkins -> Docker/EC2 -> Auto-Scaling -> New Relic -> S3

### Tech Stack
* Infra - CDK stack
* App - Node.js or Python Web app on EC2
* CI/CD - Jenkins
* Monitoring - New Relic
* Observability - Lambda logs

### Step 1
Web App (see app.py, requirements.txt, Dockerfile (optional))

### Step 2
Deploy App to EC2
Install AWS CDK
```
npm install -g aws-cdk
```
Create virtual env & install dependencies
```
python3 -m venv .venv
source .venv/bin/activate
```
Install CDK Python packages
```
pip install aws-cdk-lib constructs
```
Initialize CDK app
```
mkdir cdk-vpc-ec2-s3
cd cdk-vpc-ec2-s3
cdk init app --language python
``` 
Add resources to be deployed to app (see cdk_vpc_ec2_s3_stack file)
Bootstrap CDK (only done once per region, deploys toolkit resources needed for CDK to work in that region)
```
cdk bootstrap
```
Synthesize & Deploy CDK stack
```
cdk synth
cdk deploy
```
Tear Down
```
cdk destroy
```
