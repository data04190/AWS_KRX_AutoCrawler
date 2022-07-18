import boto3
import logging

#setup simple logging for INFO
logger = logging.getLogger()        # Instance : logger, Module : logging, Method : getLogger()
logger.setLevel(logging.INFO)

# define the connection and set the region
# Instance : ec2, Module : boto3, Method : resource, Parameter : 'ec2', region_name : 'ap-northeast-2'
ec2 = boto3.resource('ec2', region_name='ap-northeast-2')

def lambda_handler(event, context):

    # All running EC2 instances.
    filters = [{
            'Name': 'tag:AutoStop',
            'Values': ['True']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]

    # Filter the instances which are stopped
    instances = ec2.instances.filter(Filters=filters)

    # Get all id of running EC2 Instances
    RunningInstances = [instance.id for instance in instances]

    # Print the instances for logging purposes
    # Print RunningInstances 

    if len(RunningInstances) > 0:
        # Perform Shutdown EC2 Instances
        shuttingDown = ec2.instances.filter(InstanceIds=RunningInstances).stop()
        print(shuttingDown)
    else:
        print("Nothing to see here")
