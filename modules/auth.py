from fastapi import FastAPI, HTTPException
import json
from modules.token import Token

class Auth:
    def login(req):
        with open('data/users.json', 'r') as file:
            users = json.load(file)

        user_data = next((user for user in users if user['username'] == req.username and user['password'] == req.password), None)

        if user_data:
            return Token.create_access_token(user_data)
        
        if not user_data:
            raise HTTPException(status_code=401, detail="Wrong username or password")
        
    ###
    # def authenticate():