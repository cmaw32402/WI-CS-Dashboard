import pandas as pd
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc
from RaceDemoVisual import plot_cs_race, plot_total_race, race_table_maker
from GenderDemoVisual import plot_gender, gender_table_maker
from LocalityDemoVisual import plot_locality, local_table_maker
from EnrollCountVisual import plot_count, count_table_maker
from EnrollPercentVisual import plot_enroll_percent, enroll_percent_table_maker
from dash import html, dcc
from dash.dependencies import Input, Output

school_codes_df = pd.read_excel(r'C:\Users\cmaw3\Desktop\WI_CS_Dashboard_24\MasterData\2020-21_MASTER.xlsx', sheet_name= 'Agg_CS',)
code_array = school_codes_df['School Code'].values
year_array = ['2016-2017', '2017-2018','2018-2019','2019-2020','2020-2021' '2021-2022','2022-2023']

#demographics page
race_df  = race_table_maker(year_array, code_array, r'C:\Users\cmaw3\Desktop\WI_CS_Dashboard_24\VisualizationData\StudentDemographics\RaceDemographics')
gender_df = gender_table_maker(year_array, code_array, r'C:\Users\cmaw3\Desktop\WI_CS_Dashboard_24\VisualizationData\StudentDemographics\GenderDemographics')
locality_df = local_table_maker(year_array, code_array, r'C:\Users\cmaw3\Desktop\WI_CS_Dashboard_24\VisualizationData\StudentDemographics\LocalityDemographics' )

#enroll page
count_df = count_table_maker(year_array, code_array, r'C:\Users\cmaw3\Desktop\WI_CS_Dashboard_24\VisualizationData\EnrollmentInfo\EnrollmentCount' )
enroll_percent_df = enroll_percent_table_maker(year_array, code_array, r'C:\Users\cmaw3\Desktop\WI_CS_Dashboard_24\VisualizationData\EnrollmentInfo\EnrollmentPercent' )

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.layout = dbc.Container([
    dbc.Navbar(
        dbc.Container([
            dbc.Nav(
                [
                    dbc.NavLink("Student Demographics", href="/student-demo", className="nav-item"),
                    dbc.NavLink("CS Enrollment", href="/enroll-info", className="nav-item"),
                    dbc.NavLink("Page 3", href="/page-3", className="nav-item"),
                    dbc.NavLink("Page 4", href="/page-4", className="nav-item"),
                ],
                className="ml-auto flex-nowrap mt-3 mt-md-0",
                navbar=True,
                style={"justify-content": "center", "flex": 1}
            ),
        ]),
        color="secondary",
        dark=True,
    ),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
], fluid=True)


page_1_layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='gender-chart', figure=plot_gender(gender_df)),
            width=5,
            className='p-0'
        ),
        dbc.Col(
            dcc.Graph(id='locality-chart', figure=plot_locality(locality_df)),
            width=5,
            className='p-0'
        ),
    ], justify='center'),
    
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='cs-race-chart', figure=plot_cs_race(race_df)),
            width=5,
            className='p-0'
            
        ),
        dbc.Col(
            dcc.Graph(id='total-race-chart', figure=plot_total_race(race_df)),
            width=5,
            className='p-0'
        ),
    ],justify='center'),
], fluid=True)

page_2_layout = dbc.Container([
    html.H1("Enrollment"),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='count_chart', figure=plot_count(count_df)),
            width=5,
            className='p-0'
        ),
        dbc.Col(
            dcc.Graph(id='percent-chart', figure=plot_enroll_percent(enroll_percent_df)),
            width=5,
            className='p-0'
        ),
        
    ], justify='center'),
   
], fluid=True)

page_3_layout = dbc.Container([
    html.H1("Page 3"),
  
], fluid=True)

page_4_layout = dbc.Container([
    html.H1("Page 4"),
   
], fluid=True)

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/student-demo':
        return page_1_layout
    elif pathname == '/enroll-info':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
        return page_4_layout
    else:
        return page_1_layout

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)