import requests
import json
import argparse




class projected_wind_solar_requests:
    base_projected_url='https://api.pjm.com/api/v1/'

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

    SOLAR_MWH_REQUESTS='solar'
    WIND_MWH_REQUESTS='wind'


  

    def projected_solar_wind_requests(self):
        projected_options=['projected_solar','projected_wind']

        for option in projected_options:
            if option=='projected_solar':
                
                params_dict={"rowCount": "25",
                "sort":"evaluated_at_utc",
                "order": "Desc",
                "startRow": "1",
                "isActiveMetadata": "true",
                "fields": "datetime_beginning_ept,datetime_beginning_utc,datetime_ending_ept,datetime_ending_utc,evaluated_at_ept,evaluated_at_utc,solar_forecast_mwh",
                "evaluated_at_ept": "2/23/2021 09:00to3/24/2021 09:00"}
                url=f"{self.base_projected_url}hourly_{self.SOLAR_MWH_REQUESTS}_power_forecast"
                
                self.projected_solar_data=requests.get(url,headers=self.headers_projected_dict,params=params_dict).json()['items']
             
            if option=="projected_wind":

                params_dict={"rowCount": "25",
                "sort":"evaluated_at_utc",
                "order": "Desc",
                "startRow": "1",
                "isActiveMetadata": "true",
                "fields": "datetime_beginning_ept,datetime_beginning_utc,datetime_ending_ept,datetime_ending_utc,evaluated_at_ept,evaluated_at_utc,wind_forecast_mwh",
                "evaluated_at_ept": "2/23/2021 09:00to3/24/2021 09:00"}
                url=f"{self.base_projected_url}hourly_{self.WIND_MWH_REQUESTS}_power_forecast"

                self.projected_wind_data=requests.get(url,headers=self.headers_projected_dict,params=params_dict).json()['items']

        self.process_projected_wind_solar_data(self.projected_solar_data,self.projected_wind_data)


    def process_projected_wind_solar_data(self,projected_solar_data,projected_wind_data):
         self.projected_dict={}

 
         for solar_dict,wind_dict in zip(projected_solar_data,self.projected_wind_data):
             print(zip(self.projected_solar_data,self.projected_wind_data))

             if solar_dict['evaluated_at_utc'] not in self.projected_dict:
                    self.projected_dict.update({solar_dict['evaluated_at_utc']:{'projected':{'solar':int(solar_dict['solar_forecast_mwh']),'wind':int(wind_dict['wind_forecast_mwh'])}}})
                 
             else:
                print(self.projected_dict[solar_dict['evaluated_at_utc']]['projected']['wind'])
                self.projected_dict[solar_dict['evaluated_at_utc']]['projected']['solar']= self.projected_dict[solar_dict['evaluated_at_utc']]['projected']['solar'] + int(solar_dict['solar_forecast_mwh'])
                self.projected_dict[wind_dict['evaluated_at_utc']]['projected']['wind']= self.projected_dict[wind_dict['evaluated_at_utc']]['projected']['wind'] + int(wind_dict['wind_forecast_mwh'])
         print(self.projected_dict)


def main():
    handler=projected_wind_solar_requests()
    handler.projected_solar_wind_requests()
    
if __name__ == "__main__":
    main()



