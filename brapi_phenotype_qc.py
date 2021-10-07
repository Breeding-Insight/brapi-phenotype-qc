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
    html.H2(id='title', children='BrAPI Phenotype QC'),
        dcc.Input(id='brapi-url', placeholder='Enter a url...', type='text', value=''),
        html.Button(id='get-studies-button', n_clicks=0, children='Get Studies'),
        html.Div(children = [
            html.Label('Select Study:', style={'font-weight': 'bold'}),
            dcc.Dropdown(id='studies-dropdown'),
        ]),
        html.Label('Save New Study:', style={'font-weight': 'bold'}),
        html.Div(children = [
            html.Label('Log message:'),
            dcc.Input(id='change-msg', type='text', size='80'),
            html.Label('Study name:'),
            dcc.Input(id='qc-study-name', type='text', size='30'),
            html.Button(id='save-study-button', n_clicks=0, children='Save New Study'),
        ]),
        dcc.Graph(id='observations-plot'),
        dcc.Store(id='brapi-url-state'),
        dcc.Store(id='brapi-observations-data'),
        dcc.Store(id='selected-observation-ids'),
        html.Div(id='selected-controls', hidden=True, children = [
            html.Button('Remove All', id='delete-all-selected'),
            html.Button('Clear Selected', id='clear-selected')
        ]),
        dt.DataTable(id='observations-table'),
        html.Div(id='no-output', hidden=True)
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

@app.callback(Output('brapi-observations-data', 'data'),
              State('brapi-observations-data', 'data'),
              State('selected-observation-ids', 'data'),
              Input(component_id='studies-dropdown', component_property= 'value'),
              State('brapi-url-state', 'data'),
              Input('delete-all-selected', 'n_clicks'))
def update_observations(observations, selected_obs_ids, selected_study, brapi_url, delete_n_clicks): # 
    ctx = dash.callback_context
    if ctx.triggered:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == 'studies-dropdown':
            if selected_study:
                brapi_service = brapi_v2.BrAPIPhenotypeService(brapi_url)
                obs_data = brapi_service.get_observations_by_study_id(selected_study)
                return obs_data.get_data_list_dict()
            return[]
        if trigger_id == 'delete-all-selected' and delete_n_clicks > 0:
            filtered_obs = [obs for obs in observations if obs['observationDbId'] not in selected_obs_ids]
            return filtered_obs
    return []
            

@app.callback(Output(component_id='observations-plot', component_property= 'figure'),
              Input('brapi-observations-data', 'data'))
def display_observations_plot(observations):
    if observations:
        obs_df = brapi_v2.dict_to_dataframe(observations)
        obs_df['value'] = pd.to_numeric(obs_df['value'], errors='coerce')
        fig = px.scatter(obs_df, x='observationTimeStamp', y='value', 
                         color='observationVariableName', custom_data=['observationDbId'],
                         marginal_x="box", marginal_y="box",
                         labels={'observationVariableName': 'Variable name'})
        fig.update_layout(title = 'Observation values over time with marginal distributions',
                          xaxis_title = 'Date',
                          yaxis_title = 'Value'
                          )
        return fig
    return px.scatter()

@app.callback(Output('selected-observation-ids', 'data'),
              Input('observations-plot', 'selectedData'),
              Input('clear-selected', 'n_clicks'))
def update_selected_observations(selected_data, clear_n_clicks):
    ctx = dash.callback_context
    if ctx.triggered:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == 'clear-selected' and clear_n_clicks and clear_n_clicks > 0:
            # would also like to clear dcc.Graph selection/highlighting but didn't find ability to
            return []
        if trigger_id == 'observations-plot' and selected_data and len(selected_data['points']) > 0:
            selected_obs_ids = [data['customdata'][0] for data in selected_data['points']]
            return selected_obs_ids
    return []

@app.callback([Output('observations-table', 'columns'),
               Output('observations-table', 'data'),
               Output('selected-controls', 'hidden')],
              Input('selected-observation-ids', 'data'),
              State('brapi-observations-data', 'data'),
              Input('delete-all-selected', 'n_clicks'))
def display_selected_data(selected_obs_ids, observations, delete_n_clicks):
    ctx = dash.callback_context
    if ctx.triggered:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == 'selected-observation-ids':
            if len(selected_obs_ids) > 0 and len(observations) > 0:
                filtered_obs = [obs for obs in observations if obs['observationDbId'] in selected_obs_ids]
                clean_obs = [{k:v for k,v in obs.items() if v} for obs in filtered_obs]
                cols=[{'name': i, 'id': i} for i in clean_obs[0].keys()]
                return cols, clean_obs, False
    return [], [], True

@app.callback(Output('qc-study-name', 'value'),
              Input('studies-dropdown', 'value'),
              State('brapi-url-state', 'data'))
def populate_new_study_name(selected_study, brapi_url):
    if selected_study:
        brapi_service = brapi_v2.BrAPIPhenotypeService(brapi_url)
        study = brapi_service.get_study_by_id(selected_study).data
        return study['studyName']+' QC'
    return ''

@app.callback(Output('no-output', 'hidden'),
              Input('save-study-button', 'n_clicks'),
              State('brapi-url-state', 'data'),
              State('change-msg', 'value'),
              State('studies-dropdown', 'value'),
              State('qc-study-name', 'value'))
def save_study(save_study_n_clicks, brapi_url, change_msg, study_id, study_name):
    if save_study_n_clicks > 0:
        copy_service = brapi_v2.BrAPICopyService(brapi_url)
        copy_service.copy_study(study_id, study_name, change_msg)
    return True

if __name__ == '__main__': 
    app.run_server(debug=True, dev_tools_silence_routes_logging = False)