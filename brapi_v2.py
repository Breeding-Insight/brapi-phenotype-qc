#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: np398
"""

import requests
import pandas as pd

def dict_to_dataframe(brapi_dict):
    return pd.DataFrame(brapi_dict)

class BrAPIClient:
    
    DEFAULT_QUERY_PARAMS = {'pageSize':'10000'}
    DEFAULT_TIMEOUT = 60

    def __init__(self, base_url=None):
        self.base_url = base_url
        
    def set_base_url(self, base_url):
        self.base_url = base_url
        
    def get(self, endpoint, params=DEFAULT_QUERY_PARAMS, timeout=DEFAULT_TIMEOUT):
        response = requests.get(self.base_url+"/brapi/v2/"+endpoint, params=params, timeout=timeout)
        return response.json()['result']['data']
    
class BrAPIPhenotypeService:
    
    def __init__(self):
        self.client = BrAPIClient()
        self.studies = []
    
    def set_brapi_base_url(self, brapi_base_url):
        self.client.set_base_url(brapi_base_url)
        
    def get_brapi_studies(self):
        self.studies = self.client.get('studies')
        
    def get_studies_dict(self):
        return self.studies
    
    def get_studies_df(self):
        return dict_to_dataframe(self.studies)



