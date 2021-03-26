import requests
import json
import argparse
import pandas as pd
from collections import Counter
import operator
import itertools


class api_requests:
    # if args.request_type=='projected_wind':
    #         request_type='wind'
    # if args.request_type=='projected_solar':
    #        request_type='solar'

    base_projected_url='https://api.pjm.com/api/v1/'

    params_dict={"rowCount": "25",
    "sort":"evaluated_at_utc",
    "order": "Desc",
    "startRow": "1",
    "isActiveMetadata": "true",
    "fields": "datetime_beginning_ept,datetime_beginning_utc,datetime_ending_ept,datetime_ending_utc,evaluated_at_ept,evaluated_at_utc",
    "evaluated_at_ept": "2/23/2021 09:00to3/24/2021 09:00"}

    headers_projected_dict ={'Host': 'api.pjm.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': '*/*',
    'Access-Control-Request-Method': 'GET',
    'Access-Control-Request-Headers': 'ocp-apim-subscription-key',
    'Origin': 'https://dataminer2.pjm.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Ocp-Apim-Subscription-Key': 'd408630449804e23b07148259c96b24a',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://dataminer2.pjm.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9'}

    SOLAR_MWH_REQUESTS='solar_forecast_mwh'
    WIND_MHW_REQUESTS='wind_forecast_mwh'

    # def make_requests(self,request_type):

    #     if self.request_type=='projected_solar':
    #         param_string=f"{self.params_dict['fields']}{self.SOLAR_MWH_REQUESTS}"
    #     else:
    #         param_string=f"{self.params_dict['fields']}{self.WIND_MWH_REQUESTS}"

  

    def projected_solar_requests(self,request_type):
        self.request_type=request_type

        if self.request_type=='projected_solar':
            self.request_type=='solar'
        
 
        fields_partial_string=f"datetime_beginning_ept,datetime_beginning_utc,datetime_ending_ept,datetime_ending_utc,evaluated_at_ept,evaluated_at_utc,solar_forecast_mwh"
        self.params_dict['fields']=fields_partial_string
        self.projected_partial_url=f'hourly_solar_power_forecast'
        self.total_projected_url=self.base_projected_url+self.projected_partial_url
        print(self.total_projected_url)
        print(self.params_dict)
        self.response_projected_solar=requests.get(self.total_projected_url,headers=self.headers_projected_dict,
        params=self.params_dict).json()['items']
        # print(self.response_projected_solar)
        # if request_type=='projected_wind':
        #     self.response_projected_wind=requests.get(self.total_projected_url,headers=self.headers_projected_dict,
        #     params=self.params_dict).json['items']
        # if request_type=='projected_solar':
        #     self.response_projected_solar=requests.get(self.total_projected_url,headers=self.headers_projected_dict,
        #     params=self.params_dict).json()['items']
        
    def projected_wind_requests(self, r_type):
        self.r_type=r_type
        if self.r_type=='projected_wind':
            self.r_type=='wind'
        fields_partial_string=f"datetime_beginning_ept,datetime_beginning_utc,datetime_ending_ept,datetime_ending_utc,evaluated_at_ept,evaluated_at_utc,wind_forecast_mwh"
        self.params_dict['fields']=fields_partial_string
        self.projected_partial_url=f'hourly_wind_power_forecast'
        self.total_projected_url=self.base_projected_url+self.projected_partial_url
        self.response_projected_wind=requests.get(self.total_projected_url,headers=self.headers_projected_dict,
        params=self.params_dict).json()['items']
    
    def process_projected_data(self,request_type,r_type):
        self.solar_dict={}
        self.request_type=request_type
        self.r_type=r_type
        if self.request_type=='projected_solar' and self.r_type=='projected_wind':
 
            for k,j in zip(self.response_projected_solar,self.response_projected_wind):
                print(zip(self.response_projected_solar,self.response_projected_wind))

                if k['evaluated_at_utc'] not in self.solar_dict:
                    self.solar_dict.update({k['evaluated_at_utc']:{'projected':{'solar':int(k['solar_forecast_mwh']),'wind':int(j['wind_forecast_mwh'])}}})
                 
                else:
                    print(self.solar_dict[k['evaluated_at_utc']]['projected']['wind'])
                    self.solar_dict[k['evaluated_at_utc']]['projected']['solar']= self.solar_dict[k['evaluated_at_utc']]['projected']['solar'] + int(k['solar_forecast_mwh'])
                    self.solar_dict[j['evaluated_at_utc']]['projected']['wind']= self.solar_dict[j['evaluated_at_utc']]['projected']['wind'] + int(j['wind_forecast_mwh'])
            print(self.solar_dict)

        # for k in self.reponse_projected_wind:
        #     if k['evaluated_at_utc']
   
def main(request_type,r_type):
    handler = api_requests()
    if request_type=='projected_solar' and r_type=='projected_wind':

        handler.projected_solar_requests(request_type)
        handler.projected_wind_requests(r_type)
        # handler.actual_requests(a_type)
        handler.process_projected_data(request_type,r_type)
        # handler.process_projected_data(request_type,r_type)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Projected and Actual Solar and Wind Data")
    parser.add_argument(
        "request_type",
        choices=["projected_solar"],
        help="Choose an operation: projected_solar or projected_wind",
    )
    parser.add_argument(
        "r_type",
    choices=['projected_wind']
    )
  

    args = parser.parse_args()
    main(args.request_type,args.r_type)        # self.process_projected_solar_data()