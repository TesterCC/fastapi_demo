# -*- coding:utf-8 -*-

from datetime import datetime
from pathlib import Path

from typing import List, Optional
from pydantic import BaseModel, ValidationError

"""
Pydantic Official Docs:
https://docs.pydantic.dev/latest

Data validation and settings management using python type annotations.
使用Python的类型注解来进行数据校验和settings管理

pydantic enforces type hints at runtime, and provides user friendly errors when data is invalid.
Pydantic可以在代码运行时提供类型提示，数据校验失败时提供友好的错误提示

Define how data should be in pure, canonical python; validate it with pydantic.
定义数据应该如何在纯规范的Python代码中保存，并用Pydantic验证它
"""

print("\033[31m1. --- Pydantic的基本用法。Pycharm可以安装Pydantic插件 ---\033[0m")


class User(BaseModel):
    id: int  # 必须字段
    name: str = "Alice Brown"  # 有默认值，为选填字段
    signup_ts: Optional[datetime] = None
    friends: List[int] = []  # 列表中元素是int类型或者可以直接转换成int类型


external_data = {
    # "id": "123x",  # will cause error
    "id": "123",  # 设置相同id的value，以最后一次设置的value为准
    "signup_ts": "2017-07-07 07:07",
    "friends": [1, 2, "3"]  # 因为 "3" 可通过 int("3") 强转为 3
}

# 通过解包的方式传入数据

user = User(**external_data)
print(user.id, user.friends)  # 实例化后调用属性
print(repr(user.signup_ts))  # repr()函数返回的是一个对象的字符串表示形式。这个表示形式通常可以通过Python的解释器重新生成该对象。
print("-" * 99)
# print(user.dict())  # 20240511 不能用，参考下面，直接用 dict() 强转
print(dict(user))
print(user.model_dump())

print("\033[31m2. --- 校验失败处理 ---\033[0m")
try:
    User(id=1, signup_ts=datetime.today(), friends=[1, 2, "not number"])
except ValidationError as e:
    print(e.json())  # eror info output as json format

print("\033[31m3. --- 模型类的的属性和方法 ---\033[0m")
# print(user.dict())  # old, current use user.model_dump()  , don't use output with warning
print(user.model_dump())
print("-" * 99)

# print(user.json())   # old, current use user.model_dump_json()
print(user.model_dump_json())
print("-" * 99)

# print(user.copy())  # 这里是浅拷贝  old, current use user.model_copy()
print(user.model_copy())  # 这里是浅拷贝

print(user.model_dump_json())
print("=" * 99)

# 这里是给实例化对象传入数据
# print(User.parse_obj(external_data))  # old, current use user.model_validate()
print(User.model_validate(external_data))  # 校验数据格式是否和模型一致
print("-" * 99)

# print(user.parse_raw(external_data))   # old, suggest json use model_validate_json, other data use model_validate,
print(User.model_validate_json('{"id": "123", "signup_ts": "2022-12-22 12:22", "friends": [1, 2, "3"]}'))
print("-" * 99)


