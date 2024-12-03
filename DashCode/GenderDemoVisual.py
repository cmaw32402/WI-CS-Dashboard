import pandas as pd
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from RaceDemoVisual import race_demo_math
from TableFilter import table_filter


def gender_table_maker(year_array, code_array, directory_path):
    df = table_filter(year_array, code_array, directory_path)
    df = race_demo_math(df)
    df = df*100
    return df

def plot_gender(df):
    trace_cs_students = go.Bar(
        x=['Male', 'Female'],
        y=[df['CS Male Percent'].values[0], df['CS Female Percent'].values[0]],
        name='CS Students',
        width=0.4,
        offsetgroup=0,
        hoverinfo='x'
    )
    
    trace_total_students = go.Bar(
        x=['Male', 'Female'],
        y=[df['Total Male Percent'].values[0], df['Total Female Percent'].values[0]],
        name='Total Students',
        width=0.4,
        offsetgroup=1,
        hoverinfo='x'
    )
    
    data = [trace_cs_students, trace_total_students]
    
    # Layout
    layout = go.Layout(
        barmode='group',
        title='Gender Distribution',
        yaxis_title='Percentage',
        template='plotly_dark',
        xaxis=dict(
            tickvals=['Male', 'Female'],
            showgrid=False
        )
    )
    
    fig = go.Figure(data=data, layout=layout)
    
    return fig

