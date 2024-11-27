from fastapi import FastAPI, Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
from modules.token import Token
import jwt
from jwt.exceptions import InvalidTokenError
from pathlib import Path
from dotenv import dotenv_values
from starlette.responses import JSONResponse
import time

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        dotenv_path = Path('./config/.env')
        config = dotenv_values(dotenv_path) 
        
        excluded_endpoint = [
            "/auth/login",
            "/auth/refresh_token"
        ]

        if request.url.path in excluded_endpoint:
            return await call_next(request)

        auth: str = request.headers.get("Authorization")
        token = auth.split(" ")[1]
        if token is None:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "No bearer token provided"})

        json_response_not_valid = JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Could not validate credentials"})
        try:
            payload = jwt.decode(token, config['SECRET_KEY'], algorithms=config['ALGORITHM'])
            
            ## check if token expire 
            if (Token.is_access_token_expired(payload["iat"])):
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "The token has expired."})

            ## addtional checks
            user_id = payload.get("sub")
            if user_id is None:
                return json_response_not_valid
            
            ## other additional checks
            # ...
            
            request.state.payload = payload
        except InvalidTokenError:
            return json_response_not_valid
        
        response = await call_next(request)
        return response
    
    def debug(self, var):
        return JSONResponse(status_code = status.HTTP_400_BAD_REQUEST, content = var)
