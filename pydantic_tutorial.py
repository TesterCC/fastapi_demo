# -*- coding:utf-8 -*-

from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
"""
Data validation and settings management using python type annotations.
使用Python的类型注解来进行数据校验和settings管理

pydantic enforces type hints at runtime, and provides user friendly errors when data is invalid.
Pydantic可以在代码运行时提供类型提示，数据校验失败时提供友好的错误提示

Define how data should be in pure, canonical python; validate it with pydantic.
定义数据应该如何在纯规范的Python代码中保存，并用Pydantic验证它
"""


class User(BaseModel):
    id: int  # 必须字段
    name: str = "Alice Brown"  # 有默认值，为选填字段
    signup_ts: Optional[datetime] = None
    friends: List[int] = []  # 列表中元素是int类型或者可以直接转换成int类型
