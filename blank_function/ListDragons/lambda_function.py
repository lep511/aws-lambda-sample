##### List Dragons
##################
import boto3
import json

s3 = boto3.client('s3','us-east-1')
ssm = boto3.client('ssm', 'us-east-1')

def lambda_handler(event, context):
    
    bucket_name = ssm.get_parameter(
        Name='dragon_data_bucket_name',
        WithDecryption=False)['Parameter']['Value']
    file_name = ssm.get_parameter(
        Name='dragon_data_file_name',
        WithDecryption=False)['Parameter']['Value']
    
    expression = "select * from s3object[*][*] s"

    if 'queryStringParameters' in event and event['queryStringParameters'] is not None:
        if 'dragonName' in event['queryStringParameters']:
            expression = "select * from S3Object[*][*] s where s.dragon_name_str =  '" + event["queryStringParameters"]['dragonName'] + "'"
        if 'family' in event['queryStringParameters']:
            expression = "select * from S3Object[*][*] s where s.family_str =  '" + event["queryStringParameters"]['family'] + "'"

    result = s3.select_object_content(
            Bucket=bucket_name,
            Key=file_name,
            ExpressionType='SQL',
            Expression=expression,
            InputSerialization={'JSON': {'Type': 'Document'}},
            OutputSerialization={'JSON': {}}
    )
    
    result_stream = []
    for event in result['Payload']:
        if 'Records' in event:
            for line in event['Records']['Payload'].decode('utf-8').strip().split("\n"):
                result_stream.append(json.loads(line))
            
        
    return {
        "statusCode": 200,
        "body": json.dumps(result_stream),
        "headers" : {"access-control-allow-origin": "*"}
    }

        
