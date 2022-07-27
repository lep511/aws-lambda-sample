##### Main Dragon
##################
import boto3
import json

def lambda_handler(event, context):
        
    s3 = boto3.client('s3')
    ssm = boto3.client('ssm', 'us-east-1')

    bucket_name = ssm.get_parameter(
        Name='dragon_data_bucket_name',
        WithDecryption=False)['Parameter']['Value']
    file_name = ssm.get_parameter(
        Name='dragon_data_file_name',
        WithDecryption=False)['Parameter']['Value']

    file_name = "newDataDragon"
    folder_name = "dragons"

    try:
        resp=s3.get_object(Bucket=bucket_name, Key=file_name)
        main_data=resp.get('Body').read()
        json_data = json.loads(main_data)
    except:
        data_into_file = b'[]'
        s3.put_object(Body=data_into_file, Bucket=bucket_name, Key=file_name)
        json_data = json.loads(data_into_file)


    resp_file=get_object(Bucket=bucket_name, Key=folder_name + "/" + new_file)
    file_data=resp_file.get('Body').read()
    json_file_data = json.loads(file_data)

    json_data.append(json_file_data)
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(json_data).encode())

