import pulumi_aws as aws
import json

from configs import FargateConfig
from helpers.utils import get_resource_name


class FargateResource:
    def __init__(self):
        fargate_container_config = FargateConfig()
        aws.ecs.Cluster(get_resource_name('cluster'))

        role = aws.iam.Role(get_resource_name('ecs-task-exec-role'),
                            assume_role_policy=json.dumps({'Version': '2008-10-17', 'Statement':
                                [{'Sid': '', 'Effect': 'Allow', 'Principal': {'Service': 'ecs-tasks.amazonaws.com'},
                                  'Action': 'sts:AssumeRole'}]}))

        aws.iam.RolePolicyAttachment(get_resource_name('ecs-task-exec-policy'), role=role.name,
                                     policy_arn='arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy')

        container_id = get_resource_name('app-container')
        task_id = get_resource_name('app-task')

        log_group = f"/ecs/{task_id}-logs"
        aws.cloudwatch.LogGroup(log_group, tags={"Name": log_group})

        aws.ecs.TaskDefinition(task_id,
                               family=task_id,
                               cpu=fargate_container_config.cpu,
                               memory=fargate_container_config.memory,
                               network_mode='awsvpc', requires_compatibilities=['FARGATE'],
                               execution_role_arn=role.arn,
                               container_definitions=json.dumps([{'name': container_id,
                                                                  'image': fargate_container_config.docker_image,
                                                                  'environment': fargate_container_config.env_vars,
                                                                  'portMappings': [
                                                                      {'containerPort': 80,
                                                                       'hostPort': 80,
                                                                       'protocol': 'tcp'}
                                                                  ],
                                                                  "logConfiguration": {
                                                                      "logDriver": "awslogs",
                                                                      "secretOptions": None,
                                                                      "options": {
                                                                          "awslogs-group": log_group,
                                                                          "awslogs-region": f"{aws.get_region().name}",
                                                                          "awslogs-stream-prefix": "ecs"
                                                                      }
                                                                  }
                                                                  }])
                               )
