import logging
import os
import time
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ecs_client = boto3.client('ecs')


def handler(event, context):
    _start_time = time.time()
    logger.info('start task execution')

    cluster = os.getenv('FARGATE_CLUSTER')
    task_definition = os.getenv('FARGATE_TASK_DEFINITION')
    container = os.getenv('FARGATE_CONTAINER')
    subnet = os.getenv('FARGATE_SUBNET')
    security_group = os.getenv('FARGATE_SG')
    execution_role = os.getenv('FARGATE_EXECUTION_ROLE')
    task_role = os.getenv('FARGATE_TASK_ROLE')

    ecs_client.run_task(
        cluster=cluster,
        count=1,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [subnet],
                'securityGroups': [
                    security_group,
                ],
                'assignPublicIp': 'ENABLED'
            }
        },
        overrides={
            'containerOverrides': [
                {
                    'name': container,
                    # 'environment': [
                    #     {
                    #         'name': 'key',
                    #         'value': 'val'
                    #     }
                    # ],
                },
            ],
            'executionRoleArn': execution_role
        },
        platformVersion='LATEST',
        propagateTags='TASK_DEFINITION',
        taskDefinition=task_definition
    )

    logger.info('end task execution. took %s', (time.time() - _start_time))
    return {'message': 'done'}
