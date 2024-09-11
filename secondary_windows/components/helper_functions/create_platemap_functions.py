#Functions to create a platemap
import pandas as pd
import re
from .readable_plate_maps import ExperimentTypeNotImplementedError

def get_serum_val_edu(df, type_value):
    """Gets corresponding serum value to treatment type"""
    if "control" in type_value:
        serum_value = df.loc[df["Type"] == type_value, "Serum"]
        return serum_value.iloc[0] * 100.0
    elif pd.isna(type_value) or not type_value:
         return pd.NA
    else:
        serum_value = df.loc[df["Type"] == "treatment", "Serum"]
        return serum_value.iloc[0] * 100.0
    
def get_treatment_val_mft(df, type_value):
    """Gets corresponding treatment1 and treatment2 values for treatment type"""
    treatment1 = df.loc[df["standard"] == "treatment1", "concentration"]
    treatment1 = treatment1.iloc[0]
    treatment2 = df.loc[df["standard"] == "treatment2", "concentration"]
    treatment2 = treatment2.iloc[0]

    treatment1 = float(re.findall(r'[.\d]+', treatment1)[0])
    treatment2 = float(re.findall(r'[.\d]+', treatment2)[0])

    if "positive control" == type_value:
        return [treatment1, treatment2]
    elif pd.isna(type_value) or not type_value:
        return [pd.NA, pd.NA]
    elif "untreated control" == type_value:
        return [0, 0]
    else:
        return [treatment1, 0]


def mft_standards_columns(multiplate_map_df, standards_df, experiment_units):
    """
    Add the treatment columns to the multiplate map
    """
    mft_df = multiplate_map_df["treatment"].apply(lambda type: get_treatment_val_mft(standards_df, type))
    mft_df = pd.DataFrame(mft_df.tolist(), columns=["treatment1_concentration (" + experiment_units + ")", "treatment2_concentration (" + experiment_units + ")"])
    final_df = pd.concat([multiplate_map_df, mft_df], axis=1)
    final_df = final_df.iloc[:, [0,1,2,3,4,7,6,5]]
    return final_df

def edu_standards_columns(multiplate_map_df, standards_df, experiment_units):
    """
    Takes treatment data from dataframe and adds corresponding serum percentage to dataframe
    """
    edu_df = multiplate_map_df["treatment"].apply(lambda type: get_serum_val_edu(standards_df, type))
    edu_df = pd.DataFrame(edu_df.tolist(), columns=["serum (percentage)"])
    final_df = pd.concat([multiplate_map_df, edu_df], axis=1)
    return final_df

def convert_combine(dict1, df1):
    """Converts df to dictionary to combine"""
    dictp = df1.to_dict('list')
    for key in dict1:
            if key in dictp:
                dict1[key].extend(dictp[key])
    for key in dictp:
            if key not in dict1:
                dict1[key] = dictp[key]

def convert_to_multiplate_map(plate_maps_path, experiment_type, experiment_units):
    """
    Converts a plate map to from wide to long format and adds rows to specify treatment concentrations

    inputs: path to plate map to convert and the type of experiment

    output: dataframe in long format with treatment data
    """
    dict = {}
    plate_map = pd.read_excel(plate_maps_path, sheet_name=None)
    for key, value in plate_map.items():
        if key == "standards":
            pass
        else:
            #turn from wide to long format
            df = value.melt(id_vars = "row", var_name = "column")
            ntreatment2_df = df['value'].apply(lambda val: pd.Series(str(val).split("\n")))
            df = pd.concat([df[['row', 'column']], ntreatment2_df], axis=1)
            df = df.rename({0: "treatment", 1: "treatment_concentration"}, axis = "columns")
            
            #add row for well and plate
            df["well"] = df["row"] + df["column"].astype(str)
            df['plate'] = int(key.split("plate")[1])
            df = df[["row", "column", "treatment", "plate", "well","treatment_concentration"]]
            
            #Turn df into dict to add all plate maps together
            convert_combine(dict, df)
    
    #convert dict back to dataframe
    df_final = pd.DataFrame.from_dict(dict)

    #Dict for experiemnt type and their coresponding function to call
    standards = {"mft": mft_standards_columns, "edu": edu_standards_columns}
    
    if experiment_type not in standards:
            ExperimentTypeNotImplementedError(experiment_type)
    else:
         pass
    #Add rows specific to experiment type
    df_final = standards[experiment_type](df_final, plate_map["standards"], experiment_units)
    #fix and remove possible units in treatment_concentration
    df_final["treatment_concentration"] = df_final.apply(lambda x: 0 if "control" in x["treatment"] else x['treatment_concentration'], axis=1)
    df_final["treatment_concentration"] = df_final["treatment_concentration"].apply(lambda val: (re.findall(r'[.\d]+', val)[0]) if isinstance(val, str) else val)
    df_final = df_final.rename({"treatment_concentration": "treatment_concentration (" + experiment_units + ")"}, axis = "columns")
    
    return df_final