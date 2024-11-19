from fastapi import FastAPI, HTTPException
import json

class Auth:
    def login(req):
        with open('data/users.json', 'r') as file:
            users = json.load(file)

        creds_matched = any(user for user in users if user['username'] == req.username and user['password'] == req.password)
        
        if creds_matched:
            return True
        
        if creds_matched == False:
            raise HTTPException(status_code=401, detail="Wrong username or password")