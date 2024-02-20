import requests
from cryptography.hazmat.primitives import serialization

def load_public_key(jwt_token):
    response = requests.get("http://localhost:5001/public-key", headers={"Authorization": jwt_token})
    response_data = response.json()  # Parse the response JSON
    public_key_pem = response_data["public_key"]  # Extract the value of "public_key" field
    public_key = serialization.load_pem_public_key(public_key_pem.encode())  # Load the PEM-encoded key
    return public_key
