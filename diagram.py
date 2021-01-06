""" An example use of the diagrams module to create an architecture diagram
similar to 'Reference Architecture: Cross Account AWS CodePipeline':

https://github.com/awslabs/aws-refarch-cross-account-pipeline
"""


from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.devtools import Codebuild, Codecommit, Codepipeline
from diagrams.aws.general import Users
from diagrams.aws.management import Cloudformation
from diagrams.aws.mobile import APIGateway
from diagrams.aws.storage import S3


with Diagram(None, filename="aws-cross-account-pipeline", show=False):
    developers = Users("Developers")

    with Cluster("Developer Account"):
        source_code = Codecommit("CodeCommit")
        source_code << Edge(label="merge pr") << developers

    with Cluster("Shared Services Account"):
        with Cluster("Pipeline"):
            pipeline = Codepipeline("CodePipeline")
            build = Codebuild("Codebuild")
        artifacts = S3("Build Artifacts")
        source_code >> Edge(label="trigger") >> pipeline
        developers >> Edge(label="manual approval") >> pipeline
        pipeline >> build >> Edge(label="yaml file") >> artifacts

    with Cluster("Test Workload Account"):
        test_stack = Cloudformation("CloudFormation")
        test_function = Lambda("Lambda")
        test_api = APIGateway("API Gateway")
        pipeline >> test_stack
        test_api >> test_function

    with Cluster("Prod Workload Account"):
        prod_stack = Cloudformation("CloudFormation")
        prod_function = Lambda("Lambda")
        prod_api = APIGateway("API Gateway")
        pipeline >> prod_stack
        prod_api >> prod_function

