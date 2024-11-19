from fastapi import FastAPI

from modules.auth import Auth
from models.request import Login as ReqLogin

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/auth/login")
async def login(req: ReqLogin):
    return Auth.login(req)

# @app.post("/auth/login2")