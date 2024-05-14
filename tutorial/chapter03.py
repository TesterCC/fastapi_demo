# -*- coding:utf-8 -*-

from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from fastapi import APIRouter, Path, Query

app03 = APIRouter()

# write in __init__.py

"""Path Parameters and Number Validations 路径参数和数字验证"""


# 函数的顺序就是路由的顺序


# e.g. GET /ch03/ smoke test
@app03.get("/", summary="smoke test", description="smoke testing")
async def hello_world():
    return {"hello": "world"}


@app03.get("/path/parameters", summary="path params 01 static")
async def path_params01():
    return {"message": "This is a static message"}


# 路径参数  here parameters is variable
# 函数的顺序就是路由的顺序，所以按现在的顺序，如果入参为parameters，会被上面那条路由解析
@app03.get("/path/{parameters}", summary="path params 02 dynamic", description="parameters is variable")
async def path_prams02(parameters: str):
    return {"message": f"This is a dynamic message: {parameters}"}


# ext 路径参数和查询参数一起使用

# '/city/{city}' {city}是路径参数; '/city/{city}?mode=xxx'  mode=xxx是查询参数
# 自增用例，要兼容不传入?mode=xxx也能解析，就应该将 mode 设置为选填，默认值None
@app03.get('/city/{city}', summary="use path param and query param",
           description="use path param and query param at the same time")
async def get_city_mode(city: str, mode: Optional[str] = None):
    return {'city': city, 'mode': mode}


# 使用枚举类
class CityName(str, Enum):
    BJ = "Beijing China"
    SH = "Shanghai China"
    SZ = "Shenzhen China"


# 枚举类型参数
@app03.get("/enum/{city}", summary="use enum example", description="define Enum class and use it as variable")
async def enum_city(city: CityName):
    if city == CityName.BJ:
        return {"city_name": city, "online": 1492, "offline": 7}
    elif city == CityName.SH:
        return {"city_name": city, "online": 971, "offline": 9}
    elif city == CityName.SZ:
        return {"city_name": city, "online": 333, "offline": 3}
    else:
        return {"city_name": city, "latest": "unknown"}


# 通过path parameters传递文件路径  路径参数 file_path 后面指定了类型path
@app03.get("/files/{file_path:path}", summary="file_path as path var", description="use file_path as path var example")
def filepath(file_path: str):
    return f"The file path is {file_path}"


# 路径参数验证
@app03.get("/path_valid/{num}", description="example for path validation")
def path_params_validate(
        # fastapi.Path专门用于校验路径参数
        num: int = Path(..., title="Your Number", description="不可描述", ge=1, le=10),  # 1 < num < 10
):
    return num


"""Query Parameters and String Validations 查询参数和字符串验证"""


@app03.get("/query", summary="get query params example", description="get query params from page and limit")
def page_limit(page: int = 1, limit: Optional[int] = None):
    # 给了默认值就是选填的参数，没给默认值就是必填参数
    if limit:
        return {"page": page, "limit": limit}
    return {"page": page}


@app03.get("/query/bool/conversion", summary="bool conversion example", description="bool conversion example")
def type_conversion(param: bool = False):
    # bool类型转换：yes on 1 True true会转换成true, 其它为false
    return param


# http://127.0.0.1:7777/ch03/query/validations?value=abcd1234&alias_name=aa&alias_name=bb&alias_name=cc
@app03.get("/query/validations")  # 长度+正则表达式验证，比如长度8-16位，以a开头。其它校验方法看Query类的源码
def query_params_validate(
    value: str = Query(..., min_length=8, max_length=16, regex="^a"),  # ...换成None就变成选填的参数；正则表达式为：以a开头
    values: List[str] = Query(["v1", "v2"], alias="alias_name")    # 列表中含字符串类型的元素，这种用法没怎么见过
):  # 多个查询参数的列表。参数别名
    return value, values


"""Request Body and Fields 请求体和字段"""


"""Request Body + Path parameters + Query parameters 多参数混合"""

