import os
import json
import random
import datetime

import boto3
from boto3.dynamodb.conditions import Key
from lambda_decorators import cors_headers

dynamodb = boto3.resource('dynamodb')

@cors_headers
def get(event, context):
    table = dynamodb.Table(os.environ['CAMPAIGN_TABLE'])
    print(event)

    # fetch todo from the database
    # result = table.get_item(
    #     Key={
    #         'id': event['pathParameters']['id']
    #     }
    # )

    res = {
        "header": "Golden morn promo",
        "message": "buy 2 to get 1 free",
        "link": "http://www.cerealquizzer.com/"
    }
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(res)
    }

    return response


@cors_headers
def fetch(event, context):
    table = dynamodb.Table(os.environ['CAMPAIGN_TABLE'])
    data = json.loads(event['body'])
    print(data)
    if 'beacon_id' not in data or 'device_id' not in data:
        logging.error("Validation Failed")
        print("Couldn't create the Campaign item because data is incomplete.")
        response = {
            "statusCode": 404,
            "body": json.dumps({
                                "message": campaign.get("Couldn't create the Campaign item because data is incomplete.")
                            })
        }

        return response
        
   
    timestamp = str(datetime.datetime.now())


    beacon_id = data['beacon_id']
    device_id = data['device_id']
    filtering_exp = Key('network').eq(beacon_id)
    result = {
        "Items": []
    }
    try:
        result = table.scan(FilterExpression=filtering_exp)
    except:
        print("beacon not on network")

    if result["Items"] == []:
        result["Items"] == ["empty"]

    campaign = random.choice(result["Items"])  #randomly select a campaign from the available ones on the network


    # saving the device information
    device_table = dynamodb.Table(os.environ['DEVICE_TABLE'])
    try:
        device_obj = device_table.get_item(
            Key={
                'device_id': device_id
            }
        )
        item = {
            'device_id': device_id,
            'beacon': beacon_id,
            'campaign': campaign.get('campaign_id'),
            'createdAt': timestamp,
            'updatedAt': timestamp,
        }
        print("saving device data............")
        device_table.put_item(Item=item)
    except:
        print('device already in database')

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps({
                            "header": campaign.get("name"),
                            "message": campaign.get("content"),
                            "link": campaign.get("link")
                        })
    }

    return response