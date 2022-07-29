##### Main Dragon
##################
import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
        
    s3 = boto3.client('s3')
    file_name = event['file_name']
    bucket_name = event['bucket_name']
    new_file = event['new_file']

    logger.info(new_file)
    
    try:
        resp = s3.get_object(Bucket=bucket_name, Key=file_name)
        main_data = resp.get('Body').read()
        json_data = json.loads(main_data)
    except:
        logger.info("## Create File")
        data_into_file = b'[]'
        s3.put_object(Body=data_into_file, Bucket=bucket_name, Key=file_name)
        json_data = json.loads(data_into_file)

    resp_file = s3.get_object(Bucket=bucket_name, Key=new_file)
    file_data = resp_file.get('Body').read()
    json_file_data = json.loads(file_data)

    json_data.append(json_file_data)
    response = s3.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(json_data).encode())
    logger.info(response)

    return {
        'statusCode': 200,
        'body': json.dumps("File saved.")
    }
