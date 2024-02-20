import base64
import json
from datetime import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

def base64url_decode(input):
    rem = len(input) % 4
    if rem > 0:
        input += '=' * (4 - rem)
    return base64.urlsafe_b64decode(input)

def verify_jwt(jwt_token, public_key):
    segments = jwt_token.split('.')
    header, payload, signature = segments

    decoded_payload = json.loads(base64url_decode(payload).decode())

    if 'exp' not in decoded_payload:
        return {"error": "JWT token does not contain expiration ('exp') claim"}

    if datetime.utcnow().timestamp() <= decoded_payload['exp']:
        decoded_signature = base64url_decode(signature)
        signing_input = f"{header}.{payload}".encode()

        # Verify the signature using the public key
        try:
            public_key.verify(
                decoded_signature,
                signing_input,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            # Extract user_id from the decoded payload
            user_id = decoded_payload.get('user_id')
            return {"message": "JWT valid", "user_id": user_id}
        except InvalidSignature:
            return {"error": "Forbidden, JWT invalid"}

    else:
        return {"error": "Forbidden, token expired"}