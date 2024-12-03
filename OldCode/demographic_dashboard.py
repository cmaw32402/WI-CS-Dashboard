import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from studentdemographics1 import gender_table_maker, plot_cs_gender, plot_total_gender, file_paths_in_folder
from studentdemographics2 import race_table_maker, plot_cs_race, plot_total_race
import webbrowser
import dash_design_kit as ddk
# Example DataFrame
 

school_codes_df = pd.read_excel(r'C:\Users\cmaw3\Desktop\WI_CS_Dashboard_24\MasterData\2016-17_MASTER.xlsx', sheet_name= 'Agg_CS',)
school_codes = school_codes_df['School Code'].values

   
# file path array is in place of year selecting 
folder_path = r'C:\Users\cmaw3\Desktop\WI_CS_Dashboard_24/MasterData'
file_names = file_paths_in_folder(folder_path)

gender_df = gender_table_maker(file_names, school_codes)
race_df = race_table_maker(file_names, school_codes)


app = dash.Dash(__name__)

app.layout = html.Div(style={'backgroundColor': 'lightblue'}, children=[
    html.H1(children='WI CS Education Dashboard'),

    html.Div([
        html.Div(children=[
            dcc.Graph(id='cs-gender-distribution', figure=plot_cs_gender(gender_df))
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div(children=[
            dcc.Graph(id='cs-race-distribution', figure=plot_cs_race(race_df))
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    html.Div([
        html.Div(children=[
            dcc.Graph(id='total-gender-distribution', figure=plot_total_gender(gender_df))
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div(children=[
            dcc.Graph(id='total-race-distribution', figure=plot_total_race(race_df))
        ], style={'width': '48%', 'display': 'inline-block'}),
    ])
])


if __name__ == '__main__':
    webbrowser.open_new("http://127.0.0.1:8050/")
    app.run_server(debug=True)
    