# -*- coding:utf-8 -*-

from typing import Optional

from fastapi import FastAPI, BackgroundTasks, Request, APIRouter, status, HTTPException, applications
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

# 这里不一定是app，名字随意
# swagger可用，redoc貌似只读且无法操作
app = FastAPI(
    # title='FastAPI Tutorial',
    # description='Fast API Docs',
    # version='0.0.1',
    # docs_url='/docs',
    # redoc_url='/redocs',
)

# add static path, for local use swagger-ui file
app.mount("/static", StaticFiles(directory="../static"), name="static")   # attention directory path

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_ip = '0.0.0.0'
api_port = 8000

# resolve issue 1：default swagger ui cdn url can't visit, redocs cdn is of
# ref: https://www.cnblogs.com/CJTARRR/p/17756327.html
def swagger_monkey_patch(*args, **kwargs):
    """
    fastapi的swagger ui默认使用国外cdn, 所以导致文档打不开, 需要对相应方法做替换
    在应用生效前, 对swagger ui html做替换
    :param args:
    :param kwargs:
    :return:
    """
    return get_swagger_ui_html(
        *args, **kwargs,
        # swagger_js_url='https://cdn.staticfile.org/swagger-ui/5.11.0/swagger-ui-bundle.min.js',  # online inner cdn use
        # swagger_css_url='https://cdn.staticfile.org/swagger-ui/5.11.0/swagger-ui.min.css'
        # after config static path use, need 127.0.0.1
        swagger_js_url=f'http://127.0.0.1:{api_port}/static/swagger-ui/swagger-ui-bundle.min.js',
        swagger_css_url=f'http://127.0.0.1:{api_port}/static/swagger-ui/swagger-ui.min.css'
    )


def redocs_monkey_patch(*args, **kwargs):
    """
    fastapi的swagger ui默认使用国外cdn, 所以导致文档打不开, 需要对相应方法做替换
    在应用生效前, 对swagger ui html做替换
    :param args:
    :param kwargs:
    :return:
    """
    # after config static path use, need 127.0.0.1
    return get_redoc_html(
        *args, **kwargs,
        redoc_js_url=f'http://127.0.0.1:{api_port}/static/swagger-ui/redoc.standalone.js',
    )


applications.get_swagger_ui_html = swagger_monkey_patch
applications.get_redoc_html = redocs_monkey_patch


class CityInfo(BaseModel):
    province: str
    country: str
    is_affected: Optional[bool] = None  # 与bool的区别是默认值可以不传，默认是null
    # is_affected: bool # 表示必须给字段传值


# @app.get('/')
# def hello_world():
#     return {'hello': 'world'}
#
#
# # '/city/{city}' {city}是路径参数; '/city/{city}?mode=xxx'  mode=xxx是查询参数
# # 要兼容不传入?mode=xxx也能解析，就应该将 mode 设置为选填，默认值None
# @app.get('/city/{city}')
# def result(city: str, mode: Optional[str] = None):
#     return {'city': city, 'mode': mode}
#
#
# @app.put('/city/{city}')
# def put_result(city: str, city_info: CityInfo):
#     return {'city': city, 'country': city_info.country, 'is_affected': city_info.is_affected}


# # 异步实现, 因为下面几个函数都是返回具体的值，所以还没有需要使用await的逻辑
@app.get('/')
async def hello_world():
    return {'hello': 'world'}


# '/city/{city}' {city}是路径参数; '/city/{city}?mode=xxx'  mode=xxx是查询参数
# 要兼容不传入?mode=xxx也能解析，就应该将 mode 设置为选填，默认值None
@app.get('/city/{city}')
async def result(city: str, mode: Optional[str] = None):
    return {'city': city, 'mode': mode}


@app.put('/city/{city}')
async def put_result(city: str, city_info: CityInfo):
    return {'city': city, 'country': city_info.country, 'is_affected': city_info.is_affected}


# 启动命令：uvicorn hello_world:app --reload
