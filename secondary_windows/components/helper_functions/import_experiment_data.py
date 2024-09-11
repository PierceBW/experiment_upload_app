import json
from .load_s3 import client
import os

# Run this to get all experiments
def list_metadata_files(bucket_name):
    s3 = client
    
    # Use list_objects_v2 with Delimiter to list folders (common prefixes)
    response = s3.list_objects_v2(Bucket=bucket_name, Delimiter='/')

    if 'CommonPrefixes' in response:
        experiments = []
        for prefix in response['CommonPrefixes']:
            # Get the prefix (folder name)
            folder_name = prefix['Prefix']
            # List objects in the folder (one level deep)
            objects_response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name, Delimiter='/')
            temp = [obj['Prefix'] for obj in objects_response['CommonPrefixes']]
            experiments += temp
    else:
        print("No folders found in the bucket {}.".format(bucket_name))

    return experiments

# Specify the bucket name
bucket_name = os.getenv('bucket')

# Call the function to list metadata files one folder deep
experiments = list_metadata_files(bucket_name)


# Run this to get necessary functions: Gets the json file for an experiment in s3
def load_json_from_s3(bucket_name, key):
    s3_client = client
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        json_data = response['Body'].read().decode('utf-8')
        json_object = json.loads(json_data)
        return json_object
    except Exception as e:
        print(f"Error loading JSON file from S3: {e}")
        return None
