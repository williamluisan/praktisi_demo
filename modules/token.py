import jwt
import time
from dotenv import dotenv_values
from pathlib import Path
import datetime

class Token:
    this_user_data = {}
    this_config = {}

    def __init__():
        global this_config
        dotenv_path = Path('./config/.env')
        this_config = dotenv_values(dotenv_path) 
    __init__()

    def get_token(user_data):
        global this_user_data
        this_user_data = user_data        

        access_token = Token.create_access_token()
        refresh_token = Token.create_refresh_token()
        
        ###
        # store access token and refresh token
        # to DB
        # ...

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def is_access_token_expired(iat):
        expired_minutes_config = this_config['ACCESS_TOKEN_EXPIRE_MINUTES']
        return Token.is_expired(iat, expired_minutes_config)
    
    def is_refresh_token_expired(iat):
        expired_minutes_config = this_config['REFRESH_TOKEN_EXPIRE_MINUTES']
        return Token.is_expired(iat, expired_minutes_config)

    def is_expired(iat, expired_minutes_config):
        current_timestamp = int(time.time())
        token_expire_minutes_check = current_timestamp - iat
        token_expire_minutes_check = token_expire_minutes_check / 60
        if float(token_expire_minutes_check) > float(expired_minutes_config):
            return True
        
        return False


    def create_access_token():
        global this_user_data
        global this_config

        data = this_user_data

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
        
        access_token = jwt.encode(payload, this_config["SECRET_KEY"], algorithm=this_config["ALGORITHM"])
        return access_token
    
    def create_refresh_token():
        global this_user_data
        global this_config
        
        data = this_user_data

        issued_at = int(time.time())
        
        payload = {
            'sub': data['id'],
            'iat': issued_at
        }

        refresh_token = jwt.encode(payload, this_config["SECRET_KEY"], algorithm=this_config["ALGORITHM"]) 
        return refresh_token

