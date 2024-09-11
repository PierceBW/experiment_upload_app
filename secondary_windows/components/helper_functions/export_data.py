import os
import json
from .readme_creation import *
from .load_s3 import client, bucket_name
import tempfile
import os
from .create_platemap_functions import *
from .correct_and_update_functions import *

s3 = client

def upload_excel(dfs, dict):
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Temporary directory created at: {temp_dir}")

        for key in dfs:
            file_name = dict["metadata"]["experiment_date"] + "_plate_" + str(key) + ".xlsx"
            file_path = os.path.join(temp_dir, file_name)
            dfs[key].to_excel(file_path, index=False)                
            #Now upload the excel file to s3
            upload_path = dict["helpdata"]["full_path"] + "plate_maps/" + file_name
            s3.upload_file(file_path, bucket_name, upload_path)

def upload_data(dict):
    #Make Experiment's Folder and plate maps folder
    s3.put_object(Bucket=bucket_name, Key=(dict["helpdata"]["full_path"] + "plate_maps/"))

    #make multiplate map
    df = convert_to_multiplate_map(dict["helpdata"]["file_path"], dict["metadata"]["experiment_type"], dict["helpdata"]["experiment_units"])
    df = update_multiplate_map(df)

    #dict of dataframes that i go through and put in the metadata file
    dfs = {plate: group_df for plate, group_df in df.groupby('plate')}
    for key in dfs:
        dict["metadata"]["plate_data"].update(
            {str(key) : {'plate_status': '', 'plate_date': '', 'old_path_images': '', 'old_path_processed': '', 'imaging_datetime': '', 
                        'cellprofiler_data': "", 'plate_full_name': '', 'plate_map': dfs[key].to_dict()}})
    
    #put in readable plate maps: {date}_plate_{plate number}.xlsx
    upload_excel(dfs, dict)
    
    #Now put in Metadata.json file
    json_data = json.dumps(dict['metadata'])
    s3.put_object(Bucket=bucket_name, Key=(dict["helpdata"]["full_path"] + "metadata.json"), Body=json_data)

    #Now put readme file in this folder
    #import functions from readme_creation and then uncomment this
    create_readme(dict["helpdata"]["full_path"], bucket_name) #this is experiment path

    return dict


