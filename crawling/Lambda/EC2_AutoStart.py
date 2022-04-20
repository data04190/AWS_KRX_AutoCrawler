import boto3
import logging
import json
import io
import pandas as pd
from datetime import datetime
import pytz

bucket = "kmk-practice" 
file_name = "KRX_holiday_calendar.csv"

s3 = boto3.client('s3')
obj = s3.get_object(Bucket= bucket, Key= file_name)

df = pd.read_csv(obj['Body'])
list = list(df['일자 및 요일'])
print(list)

tz = pytz.timezone('Asia/Seoul')
raw_dates = datetime.now(tz)
today = raw_dates.strftime('%Y-%m-%d')

# setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# define the connection
ec2 = boto3.resource('ec2', region_name='ap-northeast-2')

def lambda_handler(event, context):

    # all stopped EC2 instances.
    filters = [{
            'Name': 'tag:AutoStart',
            'Values': ['True']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['stopped']
        }
    ]

    # filter the instances
    instances = ec2.instances.filter(Filters=filters)

    # locate all stopped instances
    RunningInstances = [instance.id for instance in instances]

    # print StoppedInstances 
    if today not in list:   #KRX 휴정일이 아니면 작동.

        if len(RunningInstances) > 0:
            # perform the startup
            AutoStarting = ec2.instances.filter(InstanceIds=RunningInstances).start()
            print("AutoStarting")
        else:
            print("Nothing to see here")
