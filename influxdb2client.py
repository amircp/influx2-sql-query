import time
import httpx
import pandas as pd
# import modin.pandas as pd

class InfluxQLClient:

    def __init__(self, host, bucket, token):
        self.host = host
        self.bucket = bucket
        self.token = token        

    def query(self, query):
        custom_header = {
            "Authorization": f"Token {self.token}"
        }
        params = {
            "db": self.bucket
        }
        self.r = httpx.post("".join([self.host,"/query"]) , 
                        headers=custom_header,
                        params=params,
                        data={"q":query})
        self.r.raise_for_status()
        return self
    
    def as_json(self):
        if self.r:
            return self.r.json()
        
        raise ValueError("No data from influxdb available")
    
    def as_dataframe(self):
        if self.r:
            json_data = self.r.json()
            print(json_data)
            results = json_data.get('results', {"series":[]})
            series = results[0].get('series',[])                      

            data = []
            serie_list = []

            if len(series) == 1:
                serie_list = series[0]
                values = serie_list['values']
    
                data = [value for value in values]
            elif len(series) > 0:
                serie_list = series[0]
                data = [serie['values'][0] for serie in series]

            if len(data) > 0:
                return pd.DataFrame(columns=serie_list['columns'], data=data)

