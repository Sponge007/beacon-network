import os
import json

import boto3
dynamodb = boto3.resource('dynamodb')


def get(event, context):
    table = dynamodb.Table(os.environ['NETWORK_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'network_id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'])
    }

    return response