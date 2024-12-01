from fastapi import HTTPException, status
import pika
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

    def list(limit: int = 3, page: int = 1):
        page_list = page - 1
        limit_list = page + limit - 1 # this because only using list
        users = Data.get_users_data()
        data = {
            "page": page,
            "limit": limit,
            "data": users[page_list:limit_list]
        }
        return data

    def detail(request, user_id):
        token_payload = request.state.payload

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User id is not provided."
            )

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
    
    def detail_generate_pdf(user_id):
        from cmd.api import rmq_chnl

        try:
            rmq_chnl.basic_publish(
                exchange='',
                routing_key='demo_pdf_generation',
                body=f'{user_id}'
            )
            return HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Your PDF will be generated soon and will be sent to your email"
            )
        except pika.exceptions.UnroutableError:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Broker: message could not be routed."
            )
        except Exception as e:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Broker: {e}"
            )
        