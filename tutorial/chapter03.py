# -*- coding:utf-8 -*-

from enum import Enum
from fastapi import APIRouter, Path

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
        num: int = Path(..., title="Your Number", description="不可描述", ge=1, le=10),   # 1 < num < 10
):
    return num
