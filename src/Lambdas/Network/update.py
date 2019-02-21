import json
import time
import datetime
import logging
import os

# from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def update(event, context):
    data = json.loads(event['body'])
    # if 'text' not in data or 'checked' not in data:
    #     logging.error("Validation Failed")
    #     raise Exception("Couldn't update the todo item.")
    #     return


    timestamp = str(datetime.datetime.now())
    print(event['pathParameters']['id'])
    table = dynamodb.Table(os.environ['NETWORK_TABLE'])
    result = table.get_item(
        Key={
            'network_id': event['pathParameters']['id']
        }
    )
    print(result)
    network = result['Item']
    beacons = network.get('beacons')

    if len(beacons) == int(network.get('size')):
        logging.error("Validation Failed")
        raise Exception("Couldn't update the Network item becuse maximum size exceeded.")
        return
    else:
        beacons[str(len(beacons)+1)] = data['beacon_id']
        # update the todo in the database
        result = table.update_item(
            Key={
                'network_id': event['pathParameters']['id']
            },
            ExpressionAttributeNames={
              '#beacons': 'beacons',
            },
            ExpressionAttributeValues={
              ':beacons': beacons,
              ':updatedAt': timestamp,
            },
            UpdateExpression='SET #beacons = :beacons, '
                             'updatedAt = :updatedAt',
            ReturnValues='ALL_NEW',
        )

        # create a response
        response = {
            "statusCode": 200,
            "body": json.dumps(result['Attributes'])
        }

        return response