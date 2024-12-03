from TableFilter import table_filter
import plotly.graph_objects as go
from RaceDemoVisual import race_demo_math

def enroll_percent_table_maker(year_array, code_array, directory_path):
    df = table_filter(year_array, code_array, directory_path)
    df = race_demo_math(df)
    df = df*100
    return df

def plot_enroll_percent(df):
    df['Non Cs Enrolled Percent'] = 100 - df['Enrollment Percent']
    labels = ['Enrollment Percent', 'Non Cs Enrolled Percent']
    values = df[labels].values[0]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='none', hole=.3)])
    fig.update_traces(hoverinfo= 'percent',)
    fig.update_layout(
        title_text='CS Enrollment Percnt of WI Students',
        template='plotly_dark'  ,
    )

    return fig
