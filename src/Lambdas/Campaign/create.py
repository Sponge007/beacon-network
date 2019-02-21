import json
import logging
import os
import time
import datetime
import uuid

# from src.utils import get_beacons


# import Image


import boto3
from lambda_decorators import cors_headers

# from Lambda.utils import send

dynamodb = boto3.resource('dynamodb')

@cors_headers
def create(event, context):
    data = json.loads(event['body'])
    if 'content' not in data or 'name' not in data or 'link' not in data or 'network' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the Campaign item because data is incomplete.")
        return
   
    timestamp = str(datetime.datetime.now())

    table = dynamodb.Table(os.environ['CAMPAIGN_TABLE'])

    item = {
        'campaign_id': str(uuid.uuid1()),
        'name': data['name'],
        'content': data['content'],
        'link': data['link'],
        'network': data['beacon_id'],
        # 'client_id': data['client_id'],
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }
    print("saving ............")
    # write the todo to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }
    
    return response