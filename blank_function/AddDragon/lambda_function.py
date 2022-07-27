##### Add Dragon
##################
import boto3
import json
from hashlib import sha256

def lambda_handler(event, context):
        
    s3 = boto3.client('s3')
    ssm = boto3.client('ssm', 'us-east-1')
    
    id_element = sha256(event['dragon_name_str'].encode('utf-8')).hexdigest()
    bucket_name = ssm.get_parameter(
        Name='dragon_data_bucket_name',
        WithDecryption=False)['Parameter']['Value']
    file_name = "newDataDragon"
    folder_name = "dragons"
    
    dragon_data = {
     "id": json.dumps(id_element),
     "description_str":event['description_str'],
     "dragon_name_str":event['dragon_name_str'],
     "family_str":event['family_str'],
     "location_city_str":event['location_city_str'],
     "location_country_str":event['location_country_str'],
     "location_neighborhood_str":event['location_neighborhood_str'],
     "location_state_str":event['location_state_str']
    }
    
    file_name = folder_name + "/" + file_name + "-" + str(id_element).lower() + ".json"

    s3.put_object(
        Bucket=bucket_name, 
        Key=file_name, 
        Body=json.dumps(dragon_data, indent=4, sort_keys=True).encode()
    )

    return {
        'statusCode': 200,
        'body': json.dumps("Dragon correct ingested.")
    }