from dotenv import load_dotenv
import urllib.parse as urlparse
import requests
import json
import os

# Requires 
class UntappdApi:

    _clientId = os.getenv("CLIENT_ID")
    _clientSecret = os.getenv("CLIENT_SECRET")
    _baseUrl = "https://api.untappd.com/v4/"
    _keys = {}

    def __init__(self, str clientId, str clientSecret):
        load_dotenv(dotenv_path="../.env")


    def keys():
        return {
            "client_id": self._clientId,
            "client_secret": self._clientSecret
        }

    def findBrewery(self, brewery="", writeFile=False):
        methodUrl = self._baseUrl + "search/brewery"
        params = {
            "q": brewery
        }
        requestUrl = methodUrl + "?" + urlparse.urlencode({**params, **self._keys})
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
        requestUrl = methodUrl + str(breweryId) + "?" + urlparse.urlencode(self._keys)
        response = requests.get(requestUrl)
        
        headers = response.headers
        counter = headers["X-Ratelimit-Remaining"]
        
        if response.status_code == 200:
            content = response.json()
            
            brewery = content["response"]
        
        return brewery, counter, response

