from fastapi import HTTPException, status, Request
from data.data import Data
from modules.token import Token
from starlette.responses import JSONResponse
from dotenv import dotenv_values
from pathlib import Path
import time
import datetime
from jwt.exceptions import InvalidTokenError
import jwt

class Auth:
    def login(req):
        ## get from db
        users = Data.get_users_data()
        user_data = next((user for user in users if user['username'] == req.username and user['password'] == req.password), None)

        if user_data:
            return Token.get_token(user_data)
        
        if not user_data:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Wrong username or password")
        
    def auth_refresh_token(req, request: Request):
        ## get from db
        users = Data.get_users_data()

        dotenv_path = Path('./config/.env')
        config = dotenv_values(dotenv_path) 

        auth: str = request.headers.get("Authorization")
        access_token = auth.split(" ")[1]
        if access_token is None:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "No bearer token provided"})

        ## check access token if expired
        json_response_not_valid = JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Could not validate credentials"})
        try: 
            payload = jwt.decode(access_token, config['SECRET_KEY'], algorithms=config['ALGORITHM'])
            if (Token.is_access_token_expired(payload["iat"]) == False):
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "The token still active"})
            
            user_data = next((user for user in users if user['name'] == payload['detail']['name'] and user['occupation'] == payload['detail']['occupation']), None)
            if user_data is None:
                return json_response_not_valid
        except InvalidTokenError:
            return json_response_not_valid

        ## check if correct refresh token
        refresh_token = req.refresh_token
        refresh_token_json_response_not_valid = JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Could not validate refresh token credentials"})
        try:
            refresh_token_payload = jwt.decode(refresh_token, config['SECRET_KEY'], algorithms=config["ALGORITHM"])

            ## check if sub same as access token
            if (payload['sub'] != refresh_token_payload['sub']):
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Wrong refresh token passed."})

            ## check refresh token if expired
            if (Token.is_refresh_token_expired(refresh_token_payload['iat']) == True):
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "The refresh token has expired."})

            ## deactivate refresh token on db
            # ...

            ## other checks
            # ...

            ## regenerate token
            return Token.get_token(user_data)
        except InvalidTokenError:
            return refresh_token_json_response_not_valid