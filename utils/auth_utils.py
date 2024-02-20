import requests

def verify_auth(jwt_token):
    response = requests.post("http://localhost:5001/auth", json={"token": jwt_token})
    data = response.json()
    return data
