import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

#function takes in a file path and produces a table 
        
def gender_table_maker(file_path):

    #two sheets with data that is needed
    student_data_sheet = '9-12 Student Data'
    sheet_name = 'Agg_CS'

    student_df = pd.read_excel(file_path, sheet_name=student_data_sheet)
    agg_df = pd.read_excel(file_path, sheet_name=sheet_name)

    # extract relevant columns
    required_columns = ['School Code', 'Academic Year', 'CS Enrolled Male Students', 'CS Enrolled Female Students']
    agg_df = agg_df[required_columns]
    
    #add column for total cs enrollment calculated by adding all available data
    agg_df['Total CS Enrollment'] = agg_df['CS Enrolled Male Students'] + agg_df['CS Enrolled Female Students']
    
    agg_df.rename(columns={'CS Enrolled Female Students': 'CS Female Percent'}, inplace=True)
    agg_df.rename(columns={'CS Enrolled Male Students': 'CS Male Percent'}, inplace=True)

    #index by school code for later merging with student df
    
    agg_df.set_index('School Code', inplace=True)
    
    for column in agg_df.columns:
        if column != 'Total CS Enrollment' and column != 'Academic Year': 
            agg_df[column] = agg_df[column] / agg_df['Total CS Enrollment']

    #agg_df = agg_df.reset_index()
    #agg_df.to_excel('aggdf.xlsx', index=False)

    #intialize and extract student sheet data
    required_columns = ['SCHOOL_CODE', 'STUDENT_RACE', 'STUDENT_GENDER']
    student_df = student_df[required_columns]
    
    #pivot based on school code to aggregate the multiple student instances in a single school
    student_df = pd.pivot_table(student_df, index='SCHOOL_CODE', columns='STUDENT_GENDER', aggfunc='size', fill_value=0)

    
    
    student_df['Total Enrollment'] = student_df['Male'] + student_df['Female']
    #rename columns so the student data df sheet can be merged to agg sheet df
    student_df.rename(columns={'Female': 'Total Female Percent'}, inplace=True)
    student_df.rename(columns={'Male': 'Total Male Percent'}, inplace=True)
    

    #calculate percentages
    for column in student_df.columns:
        if column != 'Total Enrollment': 
            student_df[column] = student_df[column] / student_df['Total Enrollment']

        
        
    #student_df = student_df.reset_index()
    #student_df.to_excel('studentdf.xlsx', index=False)

     #merge by school mode index 
     # *not sure what left index is 
     # merging is inner because keys should be intersected?
    model_df = pd.merge(agg_df, student_df, left_index=True, right_index=True, how='inner')
    model_df = model_df.reset_index()
    return model_df

#iterates through all paths and creates the normalized data files
def create_table_files():
        

    for file_path in file_paths_in_folder():
        
        table_df = gender_table_maker(file_path)
        
        #academic year taken for naming 
        academic_year = table_df['Academic Year'].iloc[0]
        file_name = f"{academic_year}GenderDemo.xlsx"
        
        #join directory path to name
        directory_path = r'C:\Users\cmaw3\Desktop\WI_CS_Dashboard_24\VisualizationData\StudentDemographics\GenderDemographics'
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