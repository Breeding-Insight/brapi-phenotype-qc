#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: np398
"""

import requests
import pandas as pd
import datetime

def dict_to_dataframe(brapi_dict):
    return pd.DataFrame(brapi_dict)

class BrAPIQueryParams:
    
    def __init__(self):
        self.params = {'pageSize':'10000'}

class BrAPIListResponse:
    
    def __init__(self, data = []):
        self.data = data
        
    def get_data_list_dict(self):
        return self.data
    
    def get_data_df(self):
        return dict_to_dataframe(self.data)
    
class BrAPISingleResponse:
    
    def __init__(self, data = {}):
        self.data = data
        
    def get_data_dict(self):
        return self.data

class BrAPIClient:
    
    DEFAULT_QUERY_PARAMS = BrAPIQueryParams().params
    DEFAULT_TIMEOUT = 60

    def __init__(self, base_url=None):
        self.base_url = base_url
        
    def set_base_url(self, base_url):
        self.base_url = base_url
        
    def __return_response_type(self, response):
        if 'data' in response.json()['result']:
            return response.json()['result']['data']
        return response.json()['result']
    
    def __form_url(self, endpoint):
        return self.base_url+"/brapi/v2/"+endpoint
        
    def get(self, endpoint, params=DEFAULT_QUERY_PARAMS, timeout=DEFAULT_TIMEOUT):
        response = requests.get(self.__form_url(endpoint), params=params, timeout=timeout)
        return self.__return_response_type(response)
    
    def post(self, endpoint, body):
        response = requests.post(self.__form_url(endpoint), json=body)
        return self.__return_response_type(response)
    
    def put(self, endpoint, body):
        response = requests.post(self.__form_url(endpoint), json=body)
        return self.__return_response_type(response)
    
class BrAPIPhenotypeService:
    
    def __init__(self, base_url):
        self.client = BrAPIClient(base_url)
    
    def set_brapi_base_url(self, brapi_base_url):
        self.client.set_base_url(brapi_base_url)
        
    def get_studies(self):
        return BrAPIListResponse(self.client.get('studies'))
    
    def get_study_by_id(self, study_id):
        return BrAPISingleResponse(self.client.get('studies'+'/'+study_id))
    
    def get_observations(self):
        return BrAPIListResponse(self.client.get('observations'))
        
    def get_observations_by_study_id(self, study_id):
        query = BrAPIQueryParams()
        query.params['studyDbId'] = study_id
        return BrAPIListResponse(self.client.get('observations', query.params))
        
    def get_observationunits_by_study_id(self, study_id):
        query = BrAPIQueryParams()
        query.params['studyDbId'] = study_id
        return BrAPIListResponse(self.client.get('observationunits', query.params))

    def post_observationunits(self, observationunits):
        return BrAPIListResponse(self.client.post('observationunits', observationunits))
    
    def post_studies(self, studies):
        return BrAPIListResponse(self.client.post('studies', studies))
    
    def put_study_by_id(self, study_id, study):
        return BrAPISingleResponse(self.client.put('studies'+'/'+study_id, study))
        
    
class BrAPICopyService:
    
    def __init__(self, from_base_url, to_base_url=None):
        self.from_brapi_service = BrAPIPhenotypeService(from_base_url)
        if not to_base_url:
            to_base_url = from_base_url
        self.to_brapi_service = BrAPIPhenotypeService(to_base_url)
        
    def copy_study(self, study_db_id, new_study_name, changelog = None, 
                   link_studies = True, link_source = 'phenotype-qc-study-ref'):
        original_study = self.from_brapi_service.get_study_by_id(study_db_id).data
        if link_studies:
            # TODO: update to be queryable
            new_study = self.__map_study(original_study, new_study_name)
            new_study['externalReferences'] = [
                    {"referenceID": original_study['studyDbId'],
                     "referenceSource": link_source
                    }
                ]
        if changelog:
            new_study['lastUpdate'] = {}
            new_study['lastUpdate']['timestamp'] = datetime.datetime.now().astimezone().isoformat()
            new_study['lastUpdate']['version'] = changelog
        return self.to_brapi_service.post_studies([new_study])
    
    def __map_study(self, original_study, new_study_name):
        new_study = original_study.copy()
        new_study['studyDbId'] = None
        new_study['studyName'] = new_study_name
        return new_study
    
class BrAPIStudyVersionService:
    
    def __init__(self, base_url):
        self.client = BrAPIClient(base_url)
        
    #TODO
