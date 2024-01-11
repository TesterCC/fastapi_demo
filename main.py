from fastapi import FastAPI
import uvicorn

app = FastAPI()


# official docs:
# https://fastapi.tiangolo.com/tutorial/first-steps/
# default docs:
# swagger http://127.0.0.1:8000/docs
# redoc http://127.0.0.1:8000/redoc
# uvicorn main:app --reload
# curl http://127.0.0.1:8000

@app.get("/")
async def index():
    return {"message": "Hello World! Let's learn FastAPI together!"}


if __name__ == '__main__':
    # manual launch in terminal
    # uvicorn main:app --reload  # default 8000

    # launch in PyCharm
    uvicorn.run("main:app", host='127.0.0.1', port=8888, reload=True)
