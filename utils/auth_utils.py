import requests

from settings import AUTH_SERVICE_URL

def verify_auth(jwt_token):
    response = requests.post(AUTH_SERVICE_URL, json={"token": jwt_token})
    data = response.json()
    return data
