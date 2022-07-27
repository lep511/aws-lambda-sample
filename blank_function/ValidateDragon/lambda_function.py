##### Validate Dragon
#####################
import boto3
from botocore.exceptions import ClientError
import json
import logging
from hashlib import sha256

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    s3 = boto3.client('s3')
    ssm = boto3.client('ssm')
    folder_name = 'dragons'
    file_base = 'newDataDragon'
    
    bucket_name = ssm.get_parameter(
        Name='dragon_data_bucket_name',
        WithDecryption=False)['Parameter']['Value']
    
    id_element = sha256(event['dragon_name_str'].encode('utf-8')).hexdigest()
    file_name = folder_name + "/" + file_base + "-" + str(id_element).lower() + ".json"

    logger.info(file_name)
    
    try:
        response = s3.head_object(Bucket=bucket_name, Key=file_name)
        file_found = True
    except ClientError as err:
        file_found = False

    if file_found:
        return {
            'statusCode': 408,
            'body': json.dumps("File exist.")
        }
    else:
        return {
            'statusCode': 200,
            'info': json.dumps("Dragon Validated."),
            'file_name': file_name,
            'bucket_name': bucket_name,
            'id_file': id_element,
            'body': event
        }
