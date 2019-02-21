import os

import boto3
dynamodb = boto3.resource('dynamodb')


def delete(event, context):
    table = dynamodb.Table(os.environ['CAMPAIGN_TABLE'])
    print(event)

    # delete the todo from the database
    table.delete_item(
        Key={
            'campaign_id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200
    }

    return response