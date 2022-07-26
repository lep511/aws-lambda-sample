##### Validate Dragon
#####################
import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3','us-east-1')
ssm = boto3.client('ssm', 'us-east-1')


def lambda_handler(event, context):
    
    bucket_name = ssm.get_parameter(
        Name='dragon_data_bucket_name',
        WithDecryption=False)['Parameter']['Value']
    file_name = ssm.get_parameter(
        Name='dragon_data_file_name',
        WithDecryption=False)['Parameter']['Value']
    
    logger.info(event['dragon_name_str'])
    
    result = s3.select_object_content(
        Bucket=bucket_name,
        Key=file_name,
        Expression="SELECT s.* FROM S3Object s WHERE s.dragon_name_str = '" + event['dragon_name_str'] + "'",
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
    
    for records in result['Payload']:
        if 'Records' in records:
            return {
                'statusCode': 408,
                'body': json.dumps("Duplicate dragon reported")
            }
    
    return {
        'statusCode': 200,
        'body': json.dumps("Dragon Validated")
    }