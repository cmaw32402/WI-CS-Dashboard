import pandas as pd
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from TableFilter import table_filter

 
def race_demo_math(df):
    filtered_df = df.drop(columns=['index', 'Academic Year'])
    filtered_df = pd.DataFrame(filtered_df.mean()).transpose()
    return filtered_df

def race_table_maker(year_array, code_array, directory_path):
    df = table_filter(year_array, code_array, directory_path)
    df = race_demo_math(df)
    return df

def plot_cs_race(df):
    labels = [
        'CS Enrolled White Students', 'CS Enrolled Black Students', 'CS Enrolled Asian Students',
        'CS Enrolled Hispanic Students', 'CS Enrolled Amer Indian Students', 'CS Enrolled Other Students'
    ]
    values = df[labels].values[0]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values,textinfo='none', hole=.3)])
    fig.update_traces(hoverinfo='percent')
    fig.update_layout(
        title_text='Race Distribution of WI CS Students',
        template='plotly_dark'  ,
        )
    
    
    return fig
   
def plot_total_race(df):
    labels = [
        'Total White Percent', 'Total Black Percent', 'Total Asian Percent',
        'Total Hispanic Percent', 'Total Amer Indian Percent', 'Other'
    ]
    values = df[labels].values[0]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='none', hole=.3)])
    fig.update_traces(hoverinfo= 'percent',)
    fig.update_layout(
        title_text='Race Distribution of WI Students',
        template='plotly_dark'  ,
    )
    return fig
    

