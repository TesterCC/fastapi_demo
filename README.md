# FastAPI notes:

## 0.Requirements
Python 3.7+

## 1.Installation

pip install fastapi -i https://pypi.tuna.tsinghua.edu.cn/simple

pip install "uvicorn[standard]" -i https://pypi.tuna.tsinghua.edu.cn/simple

pip install SQLAlchemy -i https://pypi.tuna.tsinghua.edu.cn/simple

pip install email_validator -i https://pypi.tuna.tsinghua.edu.cn/simple

pip install pytest -i https://pypi.tuna.tsinghua.edu.cn/simple

## 2.Lesson
Video: https://www.imooc.com/learn/1299
Doc: https://geek-docs.com/fastapi/fastapi-tutorials/
Git Repo: https://github.com/liaogx/fastapi-tutorial

## 3.Official
Documentation: https://fastapi.tiangolo.com/zh/tutorial/
Source Code: https://github.com/tiangolo/fastapi
Local Example: `~\git_workspace\ws_python\fastapi-tutorial`
Local Self Github repo: `~\git_workspace\ws_python\fastapi_demo`

## 4.Launch
write code in main.py, then run command: uvicorn main:app --reload

## 5.ENV
$ mkdir fastapi_demo && cd fastapi_demo
$ python3 -m venv fastapi_demo

```
# on Linux
$ source fastapi_demo/bin/activate

# on Windows
> fastapi_demo\Scripts\activate.bat

# update pip tools
python.exe -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

# update pip package
pip install -U pip setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple

# export dependencies
pip freeze > ./req.txt
```

## 6.API docs

```
# official docs:
https://fastapi.tiangolo.com/tutorial/first-steps/
# default docs:
# swagger http://127.0.0.1:8000/docs
# redoc http://127.0.0.1:8000/redoc
# uvicorn main:app --reload
# curl http://127.0.0.1:8000
```

## 7.Testcase
todo

## 8.FastAPI docker-compose 

https://stackoverflow.com/questions/70730551/pycharm-debugger-setup-with-fastapi-and-docker-compose

# 9.Todo
2-6 https://www.imooc.com/video/22981
10:30

