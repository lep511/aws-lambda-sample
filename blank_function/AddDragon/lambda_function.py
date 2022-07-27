##### Add Dragon
##################
import boto3
from botocore.exceptions import ClientError
import json

def lambda_handler(event, context):
        
    s3 = boto3.client('s3')    
    bucket_name = event['bucket_name']
    
    dragon_data = {
     "id": json.dumps(event['id_file']),
     "description_str":event['body']['description_str'],
     "dragon_name_str":event['body']['dragon_name_str'],
     "family_str":event['body']['family_str'],
     "location_city_str":event['body']['location_city_str'],
     "location_country_str":event['body']['location_country_str'],
     "location_neighborhood_str":event['body']['location_neighborhood_str'],
     "location_state_str":event['body']['location_state_str']
    }
    
    s3.put_object(
        Bucket=bucket_name, 
        Key=event['file_name'], 
        Body=json.dumps(dragon_data, indent=4, sort_keys=True).encode()
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps("Dragon correct ingested.")
    }
