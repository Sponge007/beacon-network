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
    response = {}
    print(data)
    if (data.get("name")==None or data.get("size")==None:
        response = {
            "statusCode": 404,
            "body": json.dumps({})
        }
    else:
        timestamp = str(datetime.datetime.now())

        table = dynamodb.Table(os.environ['CLIENT_TABLE'])

        item = {
            'client_id': str(uuid.uuid1()),
            'client name': data['name'],
            'client Network': data['network'],
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