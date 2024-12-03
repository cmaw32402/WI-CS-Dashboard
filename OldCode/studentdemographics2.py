import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

#function takes in a file path and produces a table 
        
def initial_table_maker(file_path, school_codes):
    #school codes to dynamically filter by district  

    #reading excel files and sheets
    student_data_sheet = '9-12 Student Data'
    sheet_name = 'Agg_CS'

    student_data_df = pd.read_excel(file_path, sheet_name=student_data_sheet)
    agg_data_df = pd.read_excel(file_path, sheet_name=sheet_name)

    # filter out by school code for agg data
    required_columns = ['Academic Year', 'School Code', 'CS Enrolled White Students', 'CS Enrolled Black Students', 'CS Enrolled Asian Students', 'CS Enrolled Hispanic Students', 'CS Enrolled Amer Indian Students', 'CS Enrolled Two or More Students', 'CS Enrolled Other Race Students']
    agg_filtered_df = agg_data_df[required_columns]
    agg_filtered_df = agg_filtered_df[agg_filtered_df['School Code'].isin(school_codes)]

    # Sum values for agg data
    cs_white = agg_filtered_df['CS Enrolled White Students'].sum()
    cs_black = agg_filtered_df['CS Enrolled Black Students'].sum()
    cs_asian =  agg_filtered_df['CS Enrolled Asian Students'].sum()
    cs_hispanic =  agg_filtered_df['CS Enrolled Hispanic Students'].sum()
    cs_nativeam =  agg_filtered_df['CS Enrolled Amer Indian Students'].sum()
    cs_other =  agg_filtered_df['CS Enrolled Two or More Students'].sum() + agg_filtered_df['CS Enrolled Other Race Students'].sum()
   # academic_year = agg_filtered_df['Academic Year']
    academic_year = agg_filtered_df['Academic Year'].values[0]
    
    #filter out by school code for student data
    required_columns = ['SCHOOL_CODE', 'STUDENT_RACE',]
    filtered_student_data_df = student_data_df[required_columns]
    filtered_student_data_df = filtered_student_data_df[filtered_student_data_df['SCHOOL_CODE'].isin(school_codes)]

    #sum values for student data
    total_white = filtered_student_data_df[filtered_student_data_df['STUDENT_RACE'] == 'White'].shape[0]
    total_black = filtered_student_data_df[filtered_student_data_df['STUDENT_RACE'] == 'Black'].shape[0]
    total_asian = filtered_student_data_df[filtered_student_data_df['STUDENT_RACE'] == 'Asian'].shape[0]
    total_hispanic = filtered_student_data_df[filtered_student_data_df['STUDENT_RACE'] == 'Hispanic'].shape[0]
    total_nativeam = filtered_student_data_df[filtered_student_data_df['STUDENT_RACE'] == 'Hispanic'].shape[0]
    total_other = filtered_student_data_df[filtered_student_data_df['STUDENT_RACE'] == 'Two or More'].shape[0]
    
     # in case of discrepencies, the total enrollment is calculated by adding m and f
    total_students = total_white + total_black + total_asian + total_hispanic + total_nativeam + total_other
    
    total_cs_students = cs_white + cs_black + cs_asian + cs_hispanic + cs_nativeam + cs_other

    data = {
        'Academic Year': academic_year,
        'CS White Percentage': [(cs_white / total_cs_students) * 100],
        'CS Black Percentage': [(cs_black / total_cs_students) * 100],
        'CS Asian Percentage': [(cs_asian / total_students) * 100],
        'CS Hispanic Percentage': [(cs_hispanic / total_students) * 100],
        'CS Nativeam Percentage': [(cs_nativeam / total_students) * 100],
        'CS Other Percentage': [(cs_other/ total_students) * 100],
        'Total White Percentage': [(total_white / total_students) * 100],
        'Total Black Percentage': [(total_black / total_students) * 100],
        'Total Asian Percentage': [( total_asian/ total_students) * 100],
        'Total Hispanic Percentage': [(total_hispanic / total_students) * 100],
        'Total Native American Percentage': [(total_nativeam / total_students) * 100],
        'Total Other Percentage': [(total_other/ total_students) * 100],
        
    }

    model_df = pd.DataFrame(data)
    return model_df

#iterates through all paths and combines tables
def race_table_maker(path_array, school_codes):
        
    #holds each files df
    final_table_array = []  

    for file_path in path_array:
        
        final_table_array.append(initial_table_maker(file_path, school_codes))   
        
    #turn array into df
    return pd.concat(final_table_array, ignore_index=False)

def plot_cs_race(df):
    labels = [
        'CS White Percentage', 'CS Black Percentage', 'CS Asian Percentage',
        'CS Hispanic Percentage', 'CS Nativeam Percentage', 'CS Other Percentage'
    ]
    values = df[labels].values[0]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title_text='CS Enrollment by Race')
    return fig
   
def plot_total_race(df):
    labels = [
        'Total White Percentage', 'Total Black Percentage', 'Total Asian Percentage',
        'Total Hispanic Percentage', 'Total Native American Percentage', 'Total Other Percentage'
    ]
    values = df[labels].values[0]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title_text='Total Student Enrollment by Race')
    return fig

school_codes_df = pd.read_excel(r'C:\Users\cmaw3\Desktop\WI_CS_Dashboard_24\MasterData\2020-21_MASTER.xlsx', sheet_name= 'Agg_CS',)
school_codes = school_codes_df['School Code'].values
   
# file path array is in place of year selecting 
file_path_array = [r'C:\Users\cmaw3\Desktop\WI_CS_Dashboard_24\MasterData\2020-21_MASTER.xlsx']
final_table = race_table_maker(file_path_array, school_codes)
#print(final_table)

plot_total_race(final_table)
plot_cs_race(final_table)