import time
import requests
import os
from dotenv import load_dotenv

# 1. opay api -> to integrate: wallet management
class OpayAPI:
    BASE_URL = "https://payapi.opayweb.com/"

    @staticmethod
    def post(endpoint, data):

        load_dotenv()
        client_auth_key = os.getenv("CLIENT_AUTH_KEY")
        version = os.getenv("VERSION")

        headers = {
            "clientAuthKey" : client_auth_key, # secret key
            "version": version, # current version
            "formatBody": "JSON", # format of request body before encryption: JSON.
            "timestamp" : str(int(time.time() * 1000 )) # current time
        }

        response = requests.post(f"{OpayAPI.BASE_URL}{endpoint}", json=data, headers=headers)
        return response.json()

# 2 smart cash api for airtel utilities purchase
class SmartCashApi:
    BASE_URL = ""

    @staticmethod
    def post(endpoint:str, data:dict):

        load_dotenv()
        # pass

        headers = {

        }
        response = requests.post(f"{SmartCashApi.BASE_URL}{endpoint}", json=data, headers=headers)
        return response.json()




# we can add many api classes as many as we need
# I don't know if bubakar or band-with finds a suitable one for us
# before I wanted to use stripe api system, but it's worldwide, unlike opay that entails only africa.
#

