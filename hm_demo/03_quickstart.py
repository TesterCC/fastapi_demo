# https://www.bilibili.com/video/BV15ktpeDEpJ?p=10

from fastapi import FastAPI

app = FastAPI()

@app.get("/home")
def home():
    return {"user_id": 1001}

@app.get("/shop")
def shop():
    return {"shop": "..."}