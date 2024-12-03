import pandas as pd
import os

def year_filter(year_array, directory_path):
    df_array = []
    for filename in os.listdir(directory_path):
        if filename[:9] in year_array:
            file_path = os.path.join(directory_path, filename)
            #read the file into a DataFrame and add it to the list
            df = pd.read_excel(file_path)  #adjust the read function based on file type
            df_array.append(df)
    final_df = pd.concat(df_array, ignore_index=False)
    return final_df

def code_filter(code_array, df):
    filtered_df = df[df['index'].isin(code_array)]
    return filtered_df

def table_filter(year_array, code_array, directory_path):
    df = year_filter(year_array, directory_path)
    df = code_filter(code_array, df)
    return df
#school_codes_df = pd.read_excel(r'C:\Users\cmaw3\Desktop\WI_CS_Dashboard_24\MasterData\2020-21_MASTER.xlsx', sheet_name= 'Agg_CS',)
#code_array = school_codes_df['School Code'].values

#directory_path = r'C:\Users\cmaw3\Desktop\WI_CS_Dashboard_24\VisualizationData\StudentDemographics\RaceDemographics'
#year_array = ['2016-2017', '2017-2018','2018-2019','2019-2020','2020-2021' '2021-2022','2022-2023']


#df = year_filter(year_array, directory_path)
#df = code_filter(code_array, df)
#print(df)