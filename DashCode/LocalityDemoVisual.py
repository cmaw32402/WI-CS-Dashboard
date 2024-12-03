import pandas as pd
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from TableFilter import table_filter

 
def locality_demo_math(df):
    filtered_df = df.drop(columns=['index', 'Academic Year'])
    filtered_df = filtered_df.groupby('Locality').sum()
    filtered_df = filtered_df.reset_index()
    return filtered_df

def local_table_maker(year_array, code_array, directory_path):
    df = table_filter(year_array, code_array, directory_path)
    df = locality_demo_math(df)
    return df

def plot_locality(df):
    trace = go.Bar(
    x=df['Locality'],
    y=df['Total CS Enrollment'],
    name='Total CS Enrollment',
    marker=dict(color='royalblue')
    )

    layout = go.Layout(
        title='Total CS Enrollment by Locality',
        xaxis=dict(title='Locality'),
        yaxis=dict(title='Total CS Enrollment'),
        template='plotly_dark',
        showlegend=True
    )

    fig = go.Figure(data=[trace], layout=layout)
    return fig


