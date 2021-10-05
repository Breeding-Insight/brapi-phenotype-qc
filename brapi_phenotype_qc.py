#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: np398
"""

import dash
import dash_html_components as html
import plotly.express as px
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table as dt
import pandas as pd
import brapi_v2

app = dash.Dash()
    
def get_study_options(studies_dict):
    return list(map(lambda study: {'label': study['studyName'], 'value': study['studyDbId']}, studies_dict))

app.layout = html.Div(id = 'parent', children = [
    html.H1(id='H1', children='BrAPI Phenotype QC', style={'textAlign':'center'}),
        dcc.Input(id='brapi-url', placeholder='Enter a url...', type='text', value=''),
        html.Button(id='get-studies-button', n_clicks=0, children='Get Studies'),
        dcc.Dropdown(id='studies-dropdown'),
        dcc.Graph(id='observations-plot'),
        dcc.Store(id='brapi-url-state'),
        dcc.Store(id='brapi-observations-data'),
        dt.DataTable(id='observations-table')
    ])

@app.callback([Output('studies-dropdown', 'options'), Output('brapi-url-state', 'data')],
              Input('get-studies-button', 'n_clicks'),
              State('brapi-url', 'value'))
def update_studies(n_clicks, brapi_url):
    if brapi_url:
        brapi_service = brapi_v2.BrAPIPhenotypeService(brapi_url)
        studies_list_dict = brapi_service.get_studies().get_data_list_dict()
        return (get_study_options(studies_list_dict), brapi_url)
    return ([], brapi_url)

@app.callback([Output(component_id='observations-plot', component_property= 'figure'),
               Output('brapi-observations-data', 'data')],
              Input(component_id='studies-dropdown', component_property= 'value'),
              Input('brapi-url-state', 'data'))
def update_observations_plot(selected_study, brapi_url):
    if selected_study:
        brapi_service = brapi_v2.BrAPIPhenotypeService(brapi_url)
        obs_data = brapi_service.get_observations_by_study_id(selected_study)
        obs_df = obs_data.get_data_df()
        obs_df['value'] = pd.to_numeric(obs_df['value'], errors='coerce')
        fig = px.scatter(obs_df, x='observationTimeStamp', y='value', custom_data=['observationDbId'])
        fig.update_layout(title = 'Observation values over time',
                          xaxis_title = 'Date',
                          yaxis_title = 'Value'
                          )
        return fig, obs_data.get_data_list_dict()
    return px.scatter(), []

@app.callback([Output('observations-table', 'columns'),
               Output('observations-table', 'data')],
              Input('observations-plot', 'selectedData'),
              Input('brapi-observations-data', 'data'))
def display_selected_data(selectedData, observations):
    if selectedData and len(selectedData['points']) > 0:
        selected_obs_ids = [data['customdata'][0] for data in selectedData['points']]
        filtered_obs = [obs for obs in observations if obs['observationDbId'] in selected_obs_ids]
        clean_obs = [{k:v for k,v in obs.items() if v} for obs in filtered_obs]
        cols=[{'name': i, 'id': i} for i in clean_obs[0].keys()]
        return cols, clean_obs
    return [], []

if __name__ == '__main__': 
    app.run_server(debug=True, dev_tools_silence_routes_logging = False)