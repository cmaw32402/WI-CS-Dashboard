import os
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
#function takes in a file path and produces a table 
        
def initial_table_maker(file_path, school_codes):
    #school codes to dynamically filter by district  

    #reading excel files and sheets
    student_data_sheet = '9-12 Student Data'
    sheet_name = 'Agg_CS'

    student_data_df = pd.read_excel(file_path, sheet_name=student_data_sheet)
    agg_data_df = pd.read_excel(file_path, sheet_name=sheet_name)

    # filter out by school code for agg data
    required_columns = ['Academic Year', 'School Code', 'CS Enrolled Male Students', 'CS Enrolled Female Students',]
    agg_filtered_df = agg_data_df[required_columns]
    agg_filtered_df = agg_filtered_df[agg_filtered_df['School Code'].isin(school_codes)]

    # Sum values for agg data
    cs_male_enrolled = agg_filtered_df['CS Enrolled Male Students'].sum()
    cs_female_enrolled = agg_filtered_df['CS Enrolled Female Students'].sum()
   # academic_year = agg_filtered_df['Academic Year']
    academic_year = agg_filtered_df['Academic Year'].values[0]
    
    #filter out by school code for student data
    required_columns = ['SCHOOL_CODE', 'STUDENT_GENDER',]
    filtered_student_data_df = student_data_df[required_columns]
    filtered_student_data_df = filtered_student_data_df[filtered_student_data_df['SCHOOL_CODE'].isin(school_codes)]

    #sum values for student data
    male_enrolled = filtered_student_data_df[filtered_student_data_df['STUDENT_GENDER'] == 'Male'].shape[0]
    female_enrolled = filtered_student_data_df[filtered_student_data_df['STUDENT_GENDER'] == 'Female'].shape[0]

     # in case of discrepencies, the total enrollment is calculated by adding m and f
    total_students = male_enrolled + female_enrolled
    
    total_cs_students = cs_male_enrolled + cs_female_enrolled

    data = {
        'Academic Year': academic_year,
        'Total CS Female Percentage': [(cs_female_enrolled / total_cs_students) * 100],
        'Total CS Male Percentage': [(cs_male_enrolled / total_cs_students) * 100],
        'Total Male Percent': [(male_enrolled / total_students) * 100],
        'Total Female Percent': [(female_enrolled / total_students) * 100],
    }

    model_df = pd.DataFrame(data)
    return model_df

#iterates through all paths and combines tables
def gender_table_maker(file_names, school_codes):
        
    #holds each files df
    final_table_array = []  

    for file in file_names:
        
        final_table_array.append(initial_table_maker(file, school_codes))   
        
    #turn array into df
    return pd.concat(final_table_array, ignore_index=False)

def plot_cs_gender(df):
   fig = px.bar(df, x="Academic Year", y=["Total CS Male Percentage", "Total CS Female Percentage"], title="Gender Distribution of CS Enrolled Students")
   pyo.plot(fig, 'my_plot.html', auto_open=True)
   return fig
   
def plot_total_gender(df):
    fig = px.bar(df, x="Academic Year", y=["Total Male Percent", "Total Female Percent"], title="Gender Distribution of WI Students")
    return fig

def file_paths_in_folder(folder_path):
    # Get a list of files in the folder
    files = os.listdir(folder_path)
    # Filter out directories and create full file paths
    file_paths = [os.path.join(folder_path, file) for file in files if os.path.isfile(os.path.join(folder_path, file))]
    return file_paths


   
# file path array is in place of year selecting 
folder_path = r'C:\Users\cmaw3\Desktop\WI_CS_Dashboard_24/MasterData'
file_names = file_paths_in_folder(folder_path)

# Example usage

