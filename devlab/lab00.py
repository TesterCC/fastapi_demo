# -*- coding:utf-8 -*-
from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field

from fastapi import APIRouter, Path, Query, Body, Cookie, Header

lab00 = APIRouter()

# write in __init__.py

"""Path Parameters and Number Validations 路径参数和数字验证"""


# 函数的顺序就是路由的顺序


# e.g. curl http://127.0.0.1:7777/lab00/
@lab00.get("/", summary="smoke test", description="smoke testing")
async def hello_world():
    return {"hello": "welcome to lab00"}


@lab00.get("/path/parameters", summary="path params 01 static")
async def path_params01():
    return {"message": "This is a static message"}


# 路径参数  here parameters is variable
# 函数的顺序就是路由的顺序，所以按现在的顺序，如果入参为parameters，会被上面那条路由解析
@lab00.get("/path/{parameters}", summary="path params 02 dynamic", description="parameters is variable")
async def path_prams02(parameters: str):
    return {"message": f"This is a dynamic message: {parameters}"}


# ext 路径参数和查询参数一起使用

# '/city/{city}' {city}是路径参数; '/city/{city}?mode=xxx'  mode=xxx是查询参数
# 自增用例，要兼容不传入?mode=xxx也能解析，就应该将 mode 设置为选填，默认值None
@lab00.get('/city/{city}', summary="use path param and query param",
           description="use path param and query param at the same time")
async def get_city_mode(city: str, mode: Optional[str] = None):
    return {'city': city, 'mode': mode}


# 使用枚举类
class CityName(str, Enum):
    BJ = "beijing"
    SH = "shanghai"
    SZ = "shenzhen"
    CD = "chengdu"
    HZ = "hangzhou"

"""
test e.g.
curl http://127.0.0.1:7777/lab00/enum/
curl http://127.0.0.1:7777/lab00/enum/test
curl http://127.0.0.1:7777/lab00/enum/beijing
"""
# 枚举类型参数
@lab00.get("/enum/{city}", summary="use enum example", description="define Enum class and use it as variable")
async def enum_city(city: CityName):
    if city == CityName.BJ:
        return {"city_name": city, "online": 1492, "offline": 7}
    elif city == CityName.SH:
        return {"city_name": city, "online": 971, "offline": 9}
    elif city == CityName.SZ:
        return {"city_name": city, "online": 333, "offline": 3}
    elif city == CityName.CD:
        return {"city_name": city, "online": 123, "offline": 10}
    elif city == CityName.HZ:
        return {"city_name": city, "online": 256, "offline": 1}
    else:
        return {"city_name": city, "latest": "unknown"}


# # 通过path parameters传递文件路径  路径参数 file_path 后面指定了类型path
# @lab00.get("/files/{file_path:path}", summary="file_path as path var", description="use file_path as path var example")
# def filepath(file_path: str):
#     return f"The file path is {file_path}"
#
#
# # 路径参数验证
# @lab00.get("/path_valid/{num}", description="example for path validation")
# def path_params_validate(
#         # fastapi.Path专门用于校验路径参数
#         num: int = Path(..., title="Your Number", description="不可描述", ge=1, le=10),  # 1 < num < 10
# ):
#     return num
#
#
# """Query Parameters and String Validations 查询参数和字符串验证"""
#
#
# @lab00.get("/query", summary="get query params example", description="get query params from page and limit")
# def page_limit(page: int = 1, limit: Optional[int] = None):
#     # 给了默认值就是选填的参数，没给默认值就是必填参数
#     if limit:
#         return {"page": page, "limit": limit}
#     return {"page": page}
#
#
# @lab00.get("/query/bool/conversion", summary="bool conversion example", description="bool conversion example")
# def type_conversion(param: bool = False):
#     # bool类型转换：yes on 1 True true会转换成true, 其它为false
#     return param
#
#
# # http://127.0.0.1:7777/ch03/query/validations?value=abcd1234&alias_name=aa&alias_name=bb&alias_name=cc
# @lab00.get("/query/validations")  # 长度+正则表达式验证，比如长度8-16位，以a开头。其它校验方法看Query类的源码
# def query_params_validate(
#         value: str = Query(..., min_length=8, max_length=16, regex="^a"),  # ...换成None就变成选填的参数；正则表达式为：以a开头
#         values: List[str] = Query(["v1", "v2"], alias="alias_name")  # 列表中含字符串类型的元素，这种用法没怎么见过
# ):  # 多个查询参数的列表。参数别名
#     return value, values
#
#
# """Request Body and Fields 请求体和字段"""
#
#
# class CityInfo(BaseModel):
#     name: str = Field(..., example="Beijing")  # example是注解的作用，值不会被验证
#     country: str
#     country_code: str = None  # 给一个默认值
#     country_population: int = Field(default=800, title="人口数量", description="国家的人口数量",
#                                     ge=800)  # display more info in swagger doc
#
#     # use sub config, can see example in swagger doc
#     class Config:
#         schema_extra = {
#             "example": {
#                 "name": "Shanghai",
#                 "country": "China",
#                 "country_code": "CN",
#                 "country_population": 1400000000,
#             }
#         }
#
#
# @lab00.post("/request_body/city", description="request body check")
# def city_info(city: CityInfo):
#     print(city.name, city.country)  # 当在IDE中输入city.的时候，属性会自动弹出
#     return city.dict()
#
#
# """3-5 Attention: Request Body + Path parameters + Query parameters 多参数混合"""
#
#
# @lab00.put("/request_body/city/{name}")
# def mix_city_info(
#         name: str,  # 城市名称
#         city01: CityInfo,
#         city02: CityInfo,  # 城市信息，Body可以是多个的  比如city02 也可以用 CityInfo2 模型
#         confirmed: int = Query(ge=0, description="确认数", default=0),
#         offline: int = Query(ge=0, description="离线数", default=0),
# ):
#     if name == "SH":
#         return {"Shanghai": {"confirmed": confirmed, "offline": offline}}
#     return city01.dict(), city02.dict()
#
#
# @lab00.put("/request_body/multiple/parameters")
# def body_multiple_parameters(
#         city: CityInfo = Body(..., embed=True),  # 当只有一个Body参数的时候，embed=True表示请求体参数嵌套。多个Body参数默认就是嵌套的
#         confirmed: int = Query(ge=0, description="确认数", default=0),
#         offline: int = Query(ge=0, description="离线数", default=0),
# ):
#     print(f"{city.name} 确认数：{confirmed} 离线数：{offline}")
#     return city.dict()
#
#
# """Request Body - Nested Models 数据格式嵌套的请求体"""
#
#
# class Data(BaseModel):
#     city: List[CityInfo] = None  # 这里就是定义数据格式嵌套的请求体
#     date: date  # 额外的数据类型，还有uuid datetime bytes frozenset等，参考：https://fastapi.tiangolo.com/tutorial/extra-data-types/
#     # 用pydantic定义请求体数据，对字段进行校验用Field类型
#     # 使用路径参数十，对字段进行校验用Path类型
#     confirmed: int = Field(ge=0, description="确认数", default=0)
#     offline: int = Field(ge=0, description="离线数", default=0)
#     recovered: int = Field(ge=0, description="恢复数", default=0)
#
#
# # 对查询参数进行校验用Query类
# @lab00.put("/request_body/nested")
# def nested_models(data: Data):
#     return data
#
#
# """Cookie 和 Header 参数"""
#
#
# # Header请求头参数自动转换的功能
# # 处理请求头中key重复的参数
# @lab00.get("/cookie")  # 效果只能用Postman测试
# def cookie(cookie_id: Optional[str] = Cookie(None)):  # 定义Cookie参数需要使用Cookie类，否则就是查询参数
#     return {"cookie_id": cookie_id}
#
#
# @lab00.get("/cookie2")  # 效果只能用Postman测试
# def cookie(cookie: Optional[str] = Cookie(None)):  # 定义Cookie参数需要使用Cookie类，否则就是查询参数
#     return {"cookie": cookie}
#
#
# @lab00.get("/header")
# def header(user_agent: Optional[str] = Header(None, convert_underscores=True), x_token: List[str] = Header(None)):
#     """这些内容会显示在swagger文档的desription中
#     有些HTTP代理和服务器是不允许在请求头中带有下划线的，所以Header提供convert_underscores属性让设置
#     :param user_agent: convert_underscores=True 会把 user_agent 变成 user-agent
#     :param x_token: x_token是包含多个值的列表
#     :return:
#     """
#     return {"User-Agent": user_agent, "x_token": x_token}
