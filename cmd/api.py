import time
import jwt
import pika
from jwt.exceptions import InvalidTokenError

from fastapi import Depends, FastAPI, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from pathlib import Path
from dotenv import dotenv_values

from modules.auth import Auth
from modules.users import Users
from middleware.JWTMiddleware import JWTMiddleware

from models.request.auth import Login as ReqLogin

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

dotenv_path = Path('./config/.env')
config = dotenv_values(dotenv_path) 

### connections
rmq = pika.BlockingConnection(pika.ConnectionParameters(config["RABBIT_MQ_URL"], config["RABBIT_MQ_PORT"]))
rmq_chnl = rmq.channel()
### //


### endpoints
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/auth/login")
async def login(req: ReqLogin):
    return Auth.login(req)

# @app.post("/auth/logout")
# async def logout(req: ReqLogout):
    # return Auth.logout(req)

# @app.post("/auth/refresh_token")
# async def refresh_token():
    # return Auth.refresh_token(req)

@app.get("/user/list")
async def user_list(limit: int = 3, page: int = 1):
    return Users.list(limit, page)

@app.get("/user/detail/{user_id}")
async def user_detail(user_id, token: Annotated[str, Depends(oauth2_scheme)]):
    return Users.detail_dummy(user_id, token)
# @app.get("/user/detail/{user_id}")
# async def user_detail(req: Request, user_id):
#     return Users.detail(req, user_id)

@app.post("/user/detail/{user_id}/generate_pdf")
async def user_detail_generate_pdf(user_id):
    return Users.detail_generate_pdf(user_id)

# return 204 no content
# @app.post("/user/update")

# return 204 no content
#@app.post("/user/delete")
### //


### middleware
app.add_middleware(JWTMiddleware)
### //