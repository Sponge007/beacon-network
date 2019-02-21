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
    print(data)

    if 'name' not in data or 'size' not in data or 'beacon' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the Network item because data is incomplete.")
        return
    timestamp = str(datetime.datetime.now())

    table = dynamodb.Table(os.environ['NETWORK_TABLE'])

    item = {
        'network_id': str(uuid.uuid1()),
        'name': data['name'],
        'size': data['size'],
        'beacons': {"1":data['beacon']},
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