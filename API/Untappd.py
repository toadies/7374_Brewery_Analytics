from dotenv import load_dotenv
import urllib.parse as urlparse
import requests
import json
import os

class Untappd:

    def __init__(self, clientId = "", clientSecret = ""):
        load_dotenv(dotenv_path="../.env")
        self._clientId = os.getenv("CLIENT_ID")
        self._clientSecret = os.getenv("CLIENT_SECRET")
        self._baseUrl = "https://api.untappd.com/v4/"


    def keys(self):
        return {
            "client_id": self._clientId,
            "client_secret": self._clientSecret
        }

    def findBrewery(self, brewery="", writeFile=False):
        methodUrl = self._baseUrl + "search/brewery"
        params = {
            "q": brewery
        }
        requestUrl = methodUrl + "?" + urlparse.urlencode({**params, **self.keys()})
        response = requests.get(requestUrl)
        
        headers = response.headers
        counter = headers["X-Ratelimit-Remaining"]
        
        if response.status_code == 200:
            content = response.json()
            
            if content["response"]["found"] > 0:
                breweries = content["response"]["brewery"]["items"]
        
        return breweries, counter, response
    
    def breweryInfo(self, breweryId="", writeFile=False):
        methodUrl = self._baseUrl + "brewery/info/"
        requestUrl = methodUrl + str(breweryId) + "?" + urlparse.urlencode(self.keys())
        response = requests.get(requestUrl)
        
        headers = response.headers
        counter = headers["X-Ratelimit-Remaining"]
        
        if response.status_code == 200:
            content = response.json()
            
            brewery = content["response"]
        
        return brewery, counter, response


