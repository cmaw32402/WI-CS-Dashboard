from TableFilter import table_filter
import plotly.graph_objects as go
import plotly.express as px
    
def count_table_maker(year_array, code_array, directory_path):
    df = table_filter(year_array, code_array, directory_path)
    df = df.pivot_table(index='Academic Year', values='Total CS Enrollment', aggfunc='sum').reset_index()
    return df

def plot_count(df):
    fig = px.line(df, x='Academic Year', y='Total CS Enrollment', title='Enrollment Over Time', markers=True)

    fig.update_yaxes(range=[0, 10000])
    fig.update_layout(
        title_text='CS Enrollment Count of WI Students',
        template='plotly_dark'  ,
    )
    return fig