##### List Dragons
##################
import boto3
import json
import os

def lambda_handler(event, context):
    
    s3 = boto3.client('s3','us-east-1')
    bucket_name = os.environ['BUCKET_NAME']
    file_name = os.environ['FILE_NAME']
    
    expression = "select * from s3object[*][*] s"

    if 'queryStringParameters' in event and event['queryStringParameters'] is not None:
        if 'dragonName' in event['queryStringParameters']:
            expression = "select * from S3Object[*][*] s where s.dragon_name_str = '" + event["queryStringParameters"]['dragonName'] + "'"
        if 'family' in event['queryStringParameters']:
            expression = "select * from S3Object[*][*] s where s.dragon_name_str =  '" + event["queryStringParameters"]['family'] + "'"

    result = s3.select_object_content(
            Bucket=bucket_name,
            Key=file_name,
            Expression=expression,
            ExpressionType='SQL',
            InputSerialization={
                'JSON': {
                    'Type': 'DOCUMENT'
                }
            },
            OutputSerialization={
                'JSON': {
                    'RecordDelimiter': ','
                }
        }
    )

    result_stream = []
    for event in result['Payload']:
        if 'Records' in event:
            for line in event['Records']['Payload'].decode('utf-8').strip().split("\n"):
                result_stream.append(json.loads(json.dumps(line)))
            
        
    return {
        "statusCode": 200,
        "body": json.dumps(result_stream),
        "headers" : {"access-control-allow-origin": "*"}
    }
