##### Add Dragon
##################
import boto3
from botocore.exceptions import ClientError
import json


def lambda_handler(event, context):
        
    s3 = boto3.client('s3')    
    bucket_name = event['bucket_name']
    file_name = event['file_name']
    new_file = event['new_file']
    id_element = event['id_file']
    
    dragon_data = {
     "id": json.dumps(id_element),
     "description_str":event['body']['description_str'],
     "dragon_name_str":event['body']['dragon_name_str'],
     "family_str":event['body']['family_str'],
     "location_city_str":event['body']['location_city_str'],
     "location_country_str":event['body']['location_country_str'],
     "location_neighborhood_str":event['body']['location_neighborhood_str'],
     "location_state_str":event['body']['location_state_str']
    }
    
    response = s3.put_object(
        Bucket=bucket_name, 
        Key=new_file, 
        Body=json.dumps(dragon_data, indent=4, sort_keys=True).encode()
    )
    res_code = response['ResponseMetadata']['HTTPStatusCode']
    
    if res_code == 200:
        return {
            'statusCode': 200,
            'bucket_name': bucket_name,
            'file_name': file_name,
            'new_file': new_file,
            'body': json.dumps("Dragon correct ingested.")
        }
    else:
        return {
            'statusCode': res_code,
            'body': json.dumps("The dragon could not be entered.")
        }
