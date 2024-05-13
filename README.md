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

## 9.课程12个核心技术点

1. 了解 FastAPI 框架特性，相对 Django/Flask 的优势
2. Pydantic 定义和规范数据格式、类型
3. 如何定义各种请求参数和验证，包括路径参数、查询参数、请求体、cookie、header
4. Jinja2 模板渲染和 Static 静态文件配置
5. FastAPI 的表单数据处理、错误处理、响应模型、文件处理、路径操作配置等
6. 全面学习 FastAPI 的依赖注入系统
7. FastAPI 的安全、认证和授权，OAuth2 认证和 JWT 认证的实现
8. FastAPI 的数据库配置与 SQLAlchemy ORM 的使用
9. 大型工程应该如何目录结构设计，多应用的文件拆分
10. FastAPI 的中间件开发
11. FastAPI 中跨域资源共享 CORS 的原理和实现方式
12. 如何编写后台任何和测试用例

# 10.Todo Learn
3-3 https://www.imooc.com/video/22984


