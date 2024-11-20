import jwt
import time
from dotenv import dotenv_values
from pathlib import Path

class Token:
    def create_access_token(data):
        dotenv_path = Path('./config/.env')
        config = dotenv_values(dotenv_path) 

        issued_at = int(time.time())

        payload = {
            'sub': data['id'], 
            'iat': issued_at,
            'detail': {
                'name': data['name'],
                'occupation': data['occupation']
            },
            'scope': [
                'write:pdf',
                'delete:pdf'    
            ]
        }
        
        jwt_encoded = jwt.encode(payload, config["SECRET_KEY"], algorithm=config["ALGORITHM"])
        
        data = {
            "access_token": jwt_encoded
        }

        return data