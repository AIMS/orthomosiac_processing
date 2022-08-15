import os

from aws_cdk import (
    # Duration,
    Stack, aws_batch, aws_batch_alpha, aws_ec2, aws_ecr_assets, aws_ecs, Environment
    # aws_sqs as sqs,
)

from constructs import Construct
vpc_id = os.getenv("VPC_ID")

class OrthomosaicProcessingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "OrthomosaicProcessingQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )


        vpc = aws_ec2.Vpc.from_lookup(self, "VPC", vpc_id=vpc_id)

        big_gpu_compute_env_resources = aws_batch_alpha.ComputeResources(
            # instance_role=ml_compute_env_instance_profile_arn,
            vpc=vpc,
            instance_types=[aws_ec2.InstanceType("g4dn.xlarge")],
            allocation_strategy=aws_batch_alpha.AllocationStrategy.SPOT_CAPACITY_OPTIMIZED,
            type=aws_batch_alpha.ComputeResourceType.SPOT

            # maxv_cpus=350,
            # compute_resources_tags={"ML_COMPUTE_ENV": "SPOT OPTIMAL"}
        )

        big_cpu_compute_env_resources = aws_batch_alpha.ComputeResources(
            vpc=vpc,
            instance_types=[aws_ec2.InstanceType("c6i.metal")],
            allocation_strategy=aws_batch_alpha.AllocationStrategy.SPOT_CAPACITY_OPTIMIZED,
            type=aws_batch_alpha.ComputeResourceType.SPOT
        )

        fast_disk_compute_env_resources = aws_batch_alpha.ComputeResources(
            vpc=vpc,
            instance_types=[aws_ec2.InstanceType("i3en.xlarge")],
            allocation_strategy=aws_batch_alpha.AllocationStrategy.SPOT_CAPACITY_OPTIMIZED,
            type=aws_batch_alpha.ComputeResourceType.SPOT
        )

        big_gpu_compute_env = aws_batch_alpha.ComputeEnvironment(
            self,
            "big_gpu_compute_env",
            enabled=True,
            managed=True,
            compute_environment_name="big_gpu_compute_env",
            compute_resources=big_gpu_compute_env_resources,
            # service_role=ml_compute_env_service_role
        )

        big_gpu_job_queue_compute_env = aws_batch_alpha.JobQueueComputeEnvironment(
            compute_environment=big_gpu_compute_env,
            order=0
        )

        big_gpu_job_queue = aws_batch_alpha.JobQueue(
            self,
            id="big_gpu_job_queue",
            compute_environments=[big_gpu_job_queue_compute_env],
            enabled=True,
            job_queue_name="big_gpu_job_queue",
            priority=10)

        metashape_image_asset = aws_ecr_assets.DockerImageAsset(
            self,
            'metashape',
            directory='batch_src/metashape_gpu',
            file='Dockerfile'
        )

        # metashape_container_image = aws_ecs.ContainerImage.from_docker_image_asset(
        #     metashape_image_asset
        # )
        #
        # metashape_container = aws_batch_alpha.JobDefinitionContainer(
        #     image=metashape_container_image,
        #     # memory_limit_mib=4096,
        #     # vcpus=4,
        #     # job_role=self.train_model_job_role,
        #     # environment={
        #     #     "DEBUG": "TRUE" if debug else "FALSE",
        #     #     "TRAINING_BUCKET": self.training_bucket.bucket_name,
        #     #     "RDS_SECRET_NAME": existing_resource_stack.db_secret.secret_name,
        #     #     "DPLAT_EVENT_LOG_ARN": existing_resource_stack.dplat_event_log_topic.topic_arn,
        #     #     "DISABLE_DPLAT_NOTIFICATIONS": "TRUE" if disable_dplat_notifications else "FALSE"
        #     # },
        #     # command=["Ref::org_name", "Ref::version"]
        # )
        #
