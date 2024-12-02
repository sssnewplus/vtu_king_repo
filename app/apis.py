import requests

# 1. opay api -> to integrate: wallet management and airtime purchase only
class OpayAPI:
    BASE_URL = "https://api.opaywallet.com/v1"

    @staticmethod
    def post(endpoint, data):
        headers = {
            "Authorization": "Bearer MY_API_KEY -> on my way to purchase it ",
            "Content-Type": "application/json",
        }
        response = requests.post(f"{OpayAPI.BASE_URL}{endpoint}", json=data, headers=headers)
        return response.json()


# we can add many api classes as many as we need
# I don't know if abubakar or bandwith finds a suitable one for us
# my colleagues please expand your thinking to find the better solution
# before I wanted to use stripe api system but it's world wide, unlike opay that entails only africa.
#

