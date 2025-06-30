# -*- coding:utf-8 -*-

from fastapi import FastAPI, BackgroundTasks, Request, APIRouter, status, HTTPException, applications
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles

import uvicorn


from tutorial import app03, app04
from devlab import lab00

# from tutorial.chapter03 import app03
# from tutorial.chapter04 import app04
# from tutorial.chapter05 import app05
# from tutorial.chapter06 import app06
# from tutorial.chapter07 import app07
# from tutorial.chapter08 import app08

# default setting
api_ip = '0.0.0.0'
api_port = 7777

# 这里不一定是app，名字随意
# swagger可用，redoc貌似只读且无法操作
app = FastAPI(
    title='FastAPI Self-learn Tutorial',
    description='API Docs',
    version='0.0.1',
    docs_url='/docs',
    redoc_url='/redocs',
)

# add static path, for local use swagger-ui file   todo 240605 look fg to change here
app.mount("/static", StaticFiles(directory="./static"), name="static")  # attention directory path


# middleware setting
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1",
        "http://127.0.0.1:8080"
        "http://localhost"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


swagger_static_ip = "127.0.0.1"

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
        swagger_js_url=f'http://{swagger_static_ip}:{api_port}/static/swagger-ui/swagger-ui-bundle.min.js',
        swagger_css_url=f'http://{swagger_static_ip}:{api_port}/static/swagger-ui/swagger-ui.min.css'
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
        redoc_js_url=f'http://{swagger_static_ip}:{api_port}/static/swagger-ui/redoc.standalone.js',
    )


applications.get_swagger_ui_html = swagger_monkey_patch
applications.get_redoc_html = redocs_monkey_patch


# add sub router
app.include_router(app03, prefix='/ch03', tags=['第三章 请求参数和验证'])
app.include_router(app04, prefix='/ch04', tags=['第四章 响应处理和FastAPI配置'])
# app.include_router(app05, prefix='/ch05', tags=['第五章 FastAPI的依赖注入系统'])
# app.include_router(app06, prefix='/ch06', tags=['第六章 安全、认证和授权'])
# app.include_router(app07, prefix='/ch07', tags=['第七章 FastAPI的数据库操作和多应用的目录结构设计'])
# app.include_router(app08, prefix='/ch08', tags=['第八章 中间件、CORS、后台任务、测试用例'])

app.include_router(lab00, prefix='/lab00', tags=['实验1 基本路由'])


if __name__ == '__main__':
    # swagger doc update need stop and start
    # cmd启动命令:
    # uvicorn run:app --host <api_ip> --port <api_port> --reload --workers 2
    # 程序启动方式
    uvicorn.run('run:app', host=api_ip, port=api_port, reload=True, workers=2)
