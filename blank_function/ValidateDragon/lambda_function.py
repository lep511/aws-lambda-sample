##### Validate Dragon
#####################
import boto3
from botocore.exceptions import ClientError
import json
import logging
from hashlib import sha256
import os
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
patch_all()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    s3 = boto3.client('s3')
    bucket_name = os.environ['BUCKET_NAME']
    file_name = os.environ['FILE_NAME']
    folder_name = 'dragons'
    file_base = 'newDataDragon'

    try:
        dragon_data = {
            "description_str":event['description_str'],
            "dragon_name_str":event['dragon_name_str'],
            "family_str":event['family_str'],
            "location_city_str":event['location_city_str'],
            "location_country_str":event['location_country_str'],
            "location_neighborhood_str":event['location_neighborhood_str'],
            "location_state_str":event['location_state_str']
        }
    except:
        return {
            'statusCode': 400,
            'body': json.dumps("Bad Request.")
        }
      
    id_element = sha256(event['dragon_name_str'].encode('utf-8')).hexdigest()
    new_file = folder_name + "/" + file_base + "-" + str(id_element).lower() + ".json"

    logger.info(new_file)
    
    try:
        response = s3.head_object(Bucket=bucket_name, Key=new_file)
        file_found = True
    except ClientError as err:
        file_found = False

    if file_found:
        return {
            'statusCode': 408,
            'body': json.dumps("File exist.")
        }
    else:
        sfn_client = boto3.client('stepfunctions')
        state_machine_arn = os.environ['STATE_MACHINE']

        response = sfn_client.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps({
                'statusCode': 200,
                'info': "Dragon Validated.",
                'file_name': file_name,
                'new_file': new_file,
                'bucket_name': bucket_name,
                'id_file': id_element,
                'body': dragon_data
                }
            )
        )
        logger.info(response)
        
        return {
            'statusCode': 200,
            'info': json.dumps("Dragon Validated.")
        }
