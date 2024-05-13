# -*- coding:utf-8 -*-
import json
from datetime import date, datetime
from pathlib import Path

from typing import List, Optional
from pydantic import BaseModel, ValidationError
from pydantic import constr
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

"""
202405: pydantic 2.5.3

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

# read json data from json file
file_path = Path("pydantic_tutorial.json")
file_path.write_text('{"id": "1234", "signup_ts": "2012-12-12 12:12", "friends": [1, 2, 3, 4]}')

# print(User.parse_file(file_path))  # 但官方已准备废弃这个方法，建议用户自己读取文件

with open('pydantic_tutorial.json', 'r') as f:
    json_data = f.read()
    print(User.model_validate_json(json_data))

print("-" * 99)

# print(user.schema())   # old
# print(user.schema_json())  # old
print(user.model_json_schema())  # 返回将模型表示为 JSON Schema 的字典, 告诉你使用的是什么数据给是的方案

print("-" * 99)

user_data = {"id": "error", "signup_ts": "2022-12-22 12 22", "friends": [1, 2, 3]}  # id是字符串 是错误的
# print(User.construct(**user_data))    # old
print(User.model_construct(**user_data))  # 不检验数据直接创建模型类，不建议在construct方法中传入未经验证的数据
# 即使入参不符合要求也不会报错，一般不推荐使用

print("-" * 99)

# print(User.__fields__.keys())  # old 定义模型类的时候，所有字段都注明类型，字段顺序就不会乱
print(User.model_fields.keys())  # 定义模型类的时候，所有字段都注明类型，字段顺序就不会乱

print("\033[31m4. --- 递归模型 ---\033[0m")  # 嵌套，就是在一个模型中调用另一个模型定义数据的格式或规范


class Sound(BaseModel):
    sound: str


class Dog(BaseModel):
    birthday: date
    weight: float = Optional[None]
    sound: List[Sound]  # 不同的狗有不同的叫声。递归模型（Recursive Models）就是指一个嵌套一个


# 嵌套的时候要做key:value
dogs = Dog(birthday=date.today(), weight=6.66, sound=[{"sound": "wang wang ~"}, {"sound": "ying ying ~"}])
print(dogs.model_dump())

print("\033[31m5. --- ORM模型：从类实例创建符合ORM对象的模型  ---\033[0m")

Base = declarative_base()


class CompanyOrm(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, nullable=False)  # 整型、主键、不能为空
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))


class CompanyModel(BaseModel):
    id: int
    public_key: constr(max_length=20)  # 限制字符串长度
    name: constr(max_length=63)
    domains: List[constr(max_length=255)]

    class Config:
        # orm_mode = True    # old
        from_attributes = True


co_orm = CompanyOrm(
    id=123,
    public_key='foobar',
    name='Testing',
    domains=['example.com', 'abc.com', 'xyz.com'],
)

# print(CompanyModel.from_orm(co_orm))   #  old
print(CompanyModel.model_validate(co_orm))

print("\033[31m6. --- Pydantic支撑的字段类型  ---\033[0m")
# 官方文档：https://pydantic-docs.helpmanual.io/usage/types/
