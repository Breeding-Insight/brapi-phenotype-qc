#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: np398
"""

import dash
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output, State
import brapi_v2

app = dash.Dash()
brapi_service = brapi_v2.BrAPIPhenotypeService()
    
def get_study_options(studies_dict):
    return list(map(lambda study: {'label': study['studyName'], 'value': study['studyDbId']}, studies_dict))

app.layout = html.Div(id = 'parent', children = [
    html.H1(id='H1', children='BrAPI Phenotype QC', style={'textAlign':'center'}),
        dcc.Input(id='brapi-url', placeholder='Enter a url...', type='text', value=''),
        html.Button(id='get-studies-button', n_clicks=0, children='Get Studies'),
        dcc.Dropdown(id='studies-dropdown', options=get_study_options(brapi_service.get_studies_dict())),
        html.Div(id='output-state'),
    ])

@app.callback(Output('studies-dropdown', 'options'),
              Input('get-studies-button', 'n_clicks'),
              State('brapi-url', 'value'))
def update_studies(n_clicks, brapi_url):
    if brapi_url:
        brapi_service.set_brapi_base_url(brapi_url)
        brapi_service.get_brapi_studies()
    return (get_study_options(brapi_service.get_studies_dict()))

if __name__ == '__main__': 
    app.run_server(debug=True, dev_tools_silence_routes_logging = False)