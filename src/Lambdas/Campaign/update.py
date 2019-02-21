import json
import time
import datetime
import logging
import os

import boto3
dynamodb = boto3.resource('dynamodb')


def update(event, context):
    data = json.loads(event['body'])
    if 'content' not in data or 'name' not in data or 'link' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the todo item.")
        return


    timestamp = str(datetime.datetime.now())

    table = dynamodb.Table(os.environ['CAMPAIGN_TABLE'])
    
    # update the todo in the database
    result = table.update_item(
        Key={
            'campaign_id': event['pathParameters']['id']
        },
        ExpressionAttributeNames={
          '#beacons': 'beacons',
        },
        ExpressionAttributeValues={
          ':beacons': beacons,
          ':content': data['content'],
          ':link': data['link'],
          ':updatedAt': timestamp,
        },
        UpdateExpression='SET #name = :name, '
                         'content = :content, '
                         'link = :link, '
                         'updatedAt = :updatedAt',
        ReturnValues='ALL_NEW',
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'])
    }

    return response