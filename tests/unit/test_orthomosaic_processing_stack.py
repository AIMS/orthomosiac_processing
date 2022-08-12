import aws_cdk as core
import aws_cdk.assertions as assertions

from orthomosaic_processing.orthomosaic_processing_stack import OrthomosaicProcessingStack

# example tests. To run these tests, uncomment this file along with the example
# resource in orthomosaic_processing/orthomosaic_processing_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = OrthomosaicProcessingStack(app, "orthomosaic-processing")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
