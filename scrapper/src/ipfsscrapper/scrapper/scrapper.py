import string

import requests


class Scrapper():
    def __init__(self, url):
        self.BASE_URL = url

    def fetch_metadata(self, CIDS: string):
        try:
            headers =  {"Content-Type":"application/json"}
            self.IPFSCIDS_URL = self.BASE_URL + CIDS
            response = requests.get(self.IPFSCIDS_URL, headers=headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Request Exception: "+ str(e))
            return None