##### List Dragons
##################
import boto3
import json


def lambda_handler(event, context):
    
    s3 = boto3.client('s3','us-east-1')
    ssm = boto3.client('ssm', 'us-east-1')

    bucket_name = ssm.get_parameter(
        Name='dragon_data_bucket_name',
        WithDecryption=False)['Parameter']['Value']
    file_name = ssm.get_parameter(
        Name='dragon_data_file_name',
        WithDecryption=False)['Parameter']['Value']
    
    expression = "SELECT s.* FROM S3Object s"

    if 'queryStringParameters' in event and event['queryStringParameters'] is not None:
        if 'dragonName' in event['queryStringParameters']:
            
            expression = "SELECT s.* FROM S3Object s WHERE s.dragon_name_str = '" + event["queryStringParameters"]['dragonName'] + "'"
        if 'family' in event['queryStringParameters']:
            expression = "SELECT s.* FROM S3Object s WHERE s.family_str =  '" + event["queryStringParameters"]['family'] + "'"

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
