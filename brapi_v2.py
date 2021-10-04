#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: np398
"""

import requests
import pandas as pd

def dict_to_dataframe(brapi_dict):
    return pd.DataFrame(brapi_dict)

class BrAPIQueryParams:
    
    def __init__(self):
        self.params = {'pageSize':'10000'}

class BrAPIDataResponse:
    
    def __init__(self, data = []):
        self.data = data
        
    def get_data_list_dict(self):
        return self.data
    
    def get_data_df(self):
        return dict_to_dataframe(self.data)

class BrAPIClient:
    
    DEFAULT_QUERY_PARAMS = BrAPIQueryParams().params
    DEFAULT_TIMEOUT = 60

    def __init__(self, base_url=None):
        self.base_url = base_url
        
    def set_base_url(self, base_url):
        self.base_url = base_url
        
    def get(self, endpoint, params=DEFAULT_QUERY_PARAMS, timeout=DEFAULT_TIMEOUT):
        print(params)
        response = requests.get(self.base_url+"/brapi/v2/"+endpoint, params=params, timeout=timeout)
        return response.json()['result']['data']
    
class BrAPIPhenotypeService:
    
    def __init__(self, base_url):
        self.client = BrAPIClient(base_url)
    
    def set_brapi_base_url(self, brapi_base_url):
        self.client.set_base_url(brapi_base_url)
        
    def get_studies(self):
        return BrAPIDataResponse(self.client.get('studies'))
    
    def get_observations(self):
        return BrAPIDataResponse(self.client.get('observations'))
        
    def get_observations_by_study_id(self, study_id):
        query = BrAPIQueryParams()
        query.params['studyDbId'] = study_id
        return BrAPIDataResponse(self.client.get('observations', query.params))
        


