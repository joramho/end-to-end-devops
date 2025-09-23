import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_vpc_ec2_s3.cdk_vpc_ec2_s3_stack import CdkVpcEc2S3Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_vpc_ec2_s3/cdk_vpc_ec2_s3_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkVpcEc2S3Stack(app, "cdk-vpc-ec2-s3")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
