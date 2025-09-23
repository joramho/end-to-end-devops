from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_autoscaling as autoscaling,
    aws_lambda as _lambda,
    aws_s3_notifications as s3n,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct

class CdkVpcEc2S3Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # 1 VPC
        vpc = ec2.Vpc(
            self, "DemoVpc",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public", subnet_type=ec2.SubnetType.PUBLIC
                )
            ]
        )

        # 2 S3 Bucket
        bucket = s3.Bucket(
            self, "DemoBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # 3 Security Group/User Data
        sg = ec2.SecurityGroup(
            self, "DemoSG",
            vpc=vpc,
            allow_all_outbound=True,
            description="Allow SSH and HTTP"
        )
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "SSH access")
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "HTTP access")

        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "yum update -y",
            "yum install -y python3 git",
            "pip3 install flask newrelic",
            "git clone https://github.com/joramho/end-to-end-devops/app.git /home/ec2-user/app",
            "cd /home/ec2-user/app",
            "newrelic-admin run-program python3 app.py"
        )

        # 4 EC2 Auto Scaling Group
        asg = autoscaling.AutoScalingGroup(
            self, "DemoASG",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            min_capacity=1,
            max_capacity=2,
            security_group=sg,
            associate_public_ip_address=True
        )
        asg.add_user_data(user_data.render())

        # 5 Lambda function triggered by S3
        function = _lambda.Function(
            self, "DemoLambda",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("lambda")
        )

        # Grant Lambda permission to read from S3
        bucket.grant_read(function)

        # Add S3 notification
        notification = s3n.LambdaDestination(function)
        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, notification)

        # 6 Outputs
        CfnOutput(self, "S3BucketName", value=bucket.bucket_name)
        CfnOutput(self, "ASGName", value=asg.auto_scaling_group_name)
