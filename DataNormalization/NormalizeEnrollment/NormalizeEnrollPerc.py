import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

#function takes in a file path and produces a table 
        
def local_table_maker(file_path):

    #two sheets with data that is needed
    sheet_name = 'Agg_CS'

    agg_df = pd.read_excel(file_path, sheet_name=sheet_name)

    # extract relevant columns
    required_columns = ['School Code', 'Academic Year', 'Total Enrollment', 'Total CS Enrollment']
    agg_df = agg_df[required_columns]
    
    agg_df.rename(columns={'School Code': 'index'}, inplace=True)

    agg_df['Enrollment Percent'] = agg_df['Total CS Enrollment']/ agg_df['Total Enrollment']
    
    return agg_df

#iterates through all paths and creates the normalized data files
def create_table_files():
        

    for file_path in file_paths_in_folder():
        
        table_df = local_table_maker(file_path)
        
        #academic year taken for naming 
        academic_year = table_df['Academic Year'].iloc[0]
        file_name = f"{academic_year}EnrollPercent.xlsx"
        
        #join directory path to name
        directory_path = r'C:\Users\cmaw3\Desktop\WI_CS_Dashboard_24\VisualizationData\EnrollmentInfo\EnrollmentPercent'
        file_path = os.path.join(directory_path, file_name)
        
        table_df.to_excel(file_path, index=False)
        print(f"DataFrame has been saved to {file_path}")

    #turn array into df

   
# file path array is in place of year selecting 
def file_paths_in_folder():
    folder_path = r'C:\Users\cmaw3\Desktop\WI_CS_Dashboard_24\MasterData'
    # get a list of files in the folder
    files = os.listdir(folder_path)
    # filter out directories and create full file paths
    file_paths = [os.path.join(folder_path, file) for file in files if os.path.isfile(os.path.join(folder_path, file))]
    return file_paths


# file path array to master data created from folder path
# never has to change because sorting data by year is handeled at later step 
#folder_path = r'C:\Users\cmaw3\Desktop\WI_CS_Dashboard_24\MasterData'
#file_path_array = file_paths_in_folder(folder_path)

create_table_files()