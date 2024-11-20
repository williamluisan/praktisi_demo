from fastapi import HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError
from dotenv import dotenv_values
from pathlib import Path
from data.data import Data

class Users:
    def get_user_detail(self, user_id):
        users = Data.get_users_data()
        user_data = next((user for user in users if user['id'] == user_id), None)
        return user_data

    def detail(request, user_id):
        token_payload = request.state.payload

        users_cls = Users()
        user = users_cls.get_user_detail(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User detail not found."
            )
        
        ### other checks if have
        # ... (permission, match with user status, etc ..)

        return user

    ## dummy function with JWT checks
    def detail_dummy(user_id, token):
        dotenv_path = Path('./config/.env')
        config = dotenv_values(dotenv_path) 
        
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, config['SECRET_KEY'], algorithms=config['ALGORITHM'])
            user_id = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        
        users_cls = Users()
        user = users_cls.get_user_detail(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User detail not found."
            )
        return user
