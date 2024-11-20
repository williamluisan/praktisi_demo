from fastapi import HTTPException, status
from data.data import Data
from modules.token import Token
from starlette.responses import JSONResponse

class Auth:
    def login(req):
        users = Data.get_users_data()

        user_data = next((user for user in users if user['username'] == req.username and user['password'] == req.password), None)

        if user_data:
            return Token.create_access_token(user_data)
        
        if not user_data:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Wrong username or password")
        
    ###
    # def authenticate():