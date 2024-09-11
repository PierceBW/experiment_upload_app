#Readme Creations
import json
from .load_s3 import client


# Run this to get necessary functions
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

def	readme_to_s3(bucket, readme_path, readme_string):
   #Write read_me string to path in s3
    s3 = client
    # Upload the JSON string to S3
    s3.put_object(Bucket=bucket, Key=readme_path, Body=readme_string)


#List of things in json to pull make sure correct plate data
get_list = ['experiment_name', 'experiment_type', 'experiment_date', 'lab_tech', 'cell_type', 'plate_data', 'experiment_description']
plate_data_get_list = ['plate_date', 'imaging_datetime']

def get_plate_data(plate_num_dict):
    plate_data_string = ""
    for numbers in plate_num_dict:
        plate_data_string += f"    Plate {numbers}:\n"
        for keys in plate_num_dict.get(numbers):
            if keys in plate_data_get_list:
                plate_data_string += f"        {keys}: {plate_num_dict.get(numbers).get(keys)}\n"
    return plate_data_string

def metadata_to_readme(metadata):
    #Pull necessary information from metadata (as a dict) and write to readme str
    readme_string = ""
    for string in get_list:
        if string in metadata:
            if string != 'plate_data':
                readme_string += f"{string}: {metadata[string]}\n"
            else:
                readme_string += f"Plates:\n"
                readme_string += get_plate_data(metadata.get('plate_data'))
    return readme_string

def create_readme(experiment_path, bucket_name):
    #create the readme string
    readme_newstring = metadata_to_readme(load_json_from_s3(bucket_name,f'{experiment_path}metadata.json'))

    #Put readme string in S3
    readme_to_s3(bucket_name, f'{experiment_path}readme.txt', readme_newstring)

    return