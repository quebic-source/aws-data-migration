import os

import pulumi


class ContainerConfig:
    def __init__(self, image, replicas, cpu, memory):
        self.image = image
        self.replicas = replicas
        self.cpu = cpu
        self.memory = memory


class FargateConfig:
    def __init__(self):
        self.cpu = pulumi.Config('fargate_container').require_int('cpu')
        self.memory = pulumi.Config('fargate_container').require_int('memory')
        self.replicas = pulumi.Config('fargate_container').require_int('replicas')
        self.vpc = pulumi.Config('fargate_container').require('vpc')
        self.subnet = pulumi.Config('fargate_container').require('subnet')
        self.docker_image = f"{os.environ['DOCKER_IMAGE']}:{os.environ['DOCKER_IMAGE_TAG']}"
        self.env_vars = [
            {
                "name": "ENVIRONMENT",
                "value": f"{pulumi.get_stack()}".upper()
            },
            {
                "name": "AWS_DEFAULT_REGION",
                "value": os.environ['AWS_DEFAULT_REGION']
            },
            {
                "name": "AWS_ACCESS_KEY_ID",
                "value": os.environ['AWS_ACCESS_KEY_ID']
            },
            {
                "name": "AWS_SECRET_ACCESS_KEY",
                "value": os.environ['AWS_SECRET_ACCESS_KEY']
            },
            {
                "name": "SOURCE_DB_USER",
                "value": os.environ['SOURCE_DB_USER']
            },
            {
                "name": "SOURCE_DB_PASSWORD",
                "value": os.environ['SOURCE_DB_PASSWORD']
            },
            {
                "name": "SOURCE_DB_HOST",
                "value": os.environ['SOURCE_DB_HOST']
            },
            {
                "name": "SOURCE_DB_DATABASE",
                "value": os.environ['SOURCE_DB_DATABASE']
            },
            {
                "name": "TARGET_DB_USER",
                "value": os.environ['TARGET_DB_USER']
            },
            {
                "name": "TARGET_DB_PASSWORD",
                "value": os.environ['TARGET_DB_PASSWORD']
            },
            {
                "name": "TARGET_DB_HOST",
                "value": os.environ['TARGET_DB_HOST']
            },
            {
                "name": "TARGET_DB_DATABASE",
                "value": os.environ['TARGET_DB_DATABASE']
            },
        ]
