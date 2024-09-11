#Functions for correcting names and updating values to include both experimental units
import pandas as pd
from pint import UnitRegistry
ureg = UnitRegistry()
import re

def correct_name(row:pd.DataFrame):
    """
    Helper function for update_multiplate_map. This will find the primary name for a row in plate map
    """
    if 'control' in row['treatment']:
        row['treatment_updated'] = row['treatment']
        row['MW (daltons)'] = pd.NA
    else:
        row['treatment_updated'] = row['primary name_x']
        row['MW (daltons)'] = row['MW (daltons)_x']
        if pd.isna(row['treatment_updated']):
            row['treatment_updated'] = row['primary name_y']
            row['MW (daltons)'] = row['MW (daltons)_y']
        if pd.isna(row['treatment_updated']):
            treatment = row['treatment']
            print(f'Missing {treatment}')
    #row = row.drop(columns=['primary name_x','secondary names_x','MW (daltons)_x','primary name_y','secondary names_y','MW (daltons)_y'])
    return row

def update_multiplate_map(multiplate_map_df, molecular_weight_df_path = "secondary_windows/components/helper_functions/molecular_weight_df.pkl"):
    """
    Correct peptide names in plate map

    Args:
        multiplate_map_df (pandas.DataFrame): plate map with treatment column
        molecular_weight_df (pandas.DataFrame): molecular weight df with primary and secondar names

    Returns:
        pandas.Dataframe: dataframe with updated peptide names
    """
    molecular_weight_df = pd.read_pickle(molecular_weight_df_path)

    multiplate_map_df = multiplate_map_df.merge(molecular_weight_df,left_on='treatment',right_on='primary name',how='left')
    multiplate_map_df = multiplate_map_df.merge(molecular_weight_df.explode('secondary names'),left_on='treatment',right_on='secondary names',how='left')
    multiplate_map_df = multiplate_map_df.apply(correct_name,axis=1).drop(columns=['primary name_x','secondary names_x','MW (daltons)_x','primary name_y','secondary names_y','MW (daltons)_y', 'treatment'])
    multiplate_map_df = multiplate_map_df.rename({"treatment_updated": "treatment"}, axis = "columns")
    # Insert the 'treatment' column at the third position (index 2)
    cols = multiplate_map_df.columns.tolist()
    cols.remove('treatment')
    cols.insert(2, 'treatment')
    multiplate_map_df = multiplate_map_df[cols]
    
    multiplate_map_df = multiplate_map_df.replace(to_replace=[None], value=pd.NA)
    return multiplate_map_df

def convert_concentration(concentration,units,molecular_weight,target_units):
    """
    Given a concentration in molarity or g/l convert to target units

    Args:
        concentration (float): numerical value of concentration
        units (str): units of concentrations
        molecular_weight (float): numerical value of molecular weight in grams/mole
        target_units (str): target units of conversion
    
    Returns:
        (float): concentration in target units
    """
    ureg.define('molarity = mol/L = M')
    units = ureg(units)
    concentration = concentration * units
    molecular_weight = molecular_weight * ureg.gram / ureg.mole

    if units.to_base_units().units == ureg('mole/meter**3').units:
        concentration = concentration * molecular_weight
    else:
        concentration = concentration / molecular_weight
    
    return round(concentration.to(target_units).magnitude,2)

convert_concentration(20,'ng/ml',24000,'nM')
def update_concentrations(multiplate_map_df, experiment_type, treatment1_mw=24000.,treatment2_mw=399.42):
    """
    Function to add missing concentration type

    Args:
        multiplate_map_df (pandas.DataFrame): Plate map in row form holding all plates from a given experiment
        treatment1_mw (float): molecular weight of treatment1 in g/mol
        treatment2_mw (float): molecular weight of treatment2 in g/mol

    Returns:
        pandas.DataFrame: return multiplate map with missing concentration types
    """
    # I want you to implement this function so missing concetration types are dynamically added.
    # If a concentration column is ng/ml create one for nM or vice versa
    unit_list = ["nM", "ng/ml"]
    #List of columns
    col = multiplate_map_df.columns.tolist()
    #Find the units
    for string in col:
        if "treatment_concentration" in string:
            units = re.findall(r'\((.*?)\)', string)[0]
    #Get opposite units
    unit_list.remove(units)
    oppUnits = unit_list[0]
    
    if experiment_type == "mft":
        # dd other treatment1 column
        multiplate_map_df["treatment2_concentration (" + oppUnits + ")"] = multiplate_map_df.apply(lambda x: convert_concentration(float(x["treatment2_concentration (" + units + ")"]), units, treatment2_mw, oppUnits), axis=1)
        #add other treatment2 column
        multiplate_map_df["treatment1_concentration (" + oppUnits + ")"] = multiplate_map_df.apply(lambda x: convert_concentration(float(x["treatment1_concentration (" + units + ")"]), units, treatment1_mw, oppUnits), axis=1)
    else:
        pass
    #add other treatment concentration column
    multiplate_map_df["treatment_concentration (" + oppUnits + ")"] = multiplate_map_df.apply(lambda x: 0 if "control" in x["treatment"] else convert_concentration(float(x["treatment_concentration (" + units + ")"]), units, x["MW (daltons)"], oppUnits), axis=1)
    
    
    return multiplate_map_df