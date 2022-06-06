import os

from main import handler

os.environ['FARGATE_CLUSTER'] = 'aws-data-migration-dev-cluster-1df295b'
os.environ['FARGATE_TASK_DEFINITION'] = 'aws-data-migration-dev-app-task:7'
os.environ['FARGATE_CONTAINER'] = 'aws-data-migration-dev-app-container'
os.environ['FARGATE_SUBNET'] = 'subnet-e6a46cd7'
os.environ['FARGATE_SG'] = 'sg-79b79b4b'
os.environ['FARGATE_EXECUTION_ROLE'] = 'arn:aws:iam::893502944061:role/aws-data-migration-dev-ecs-task-exec-role-4efe13e'

resp = handler({}, {})
print(resp)
