# -*- coding:utf-8 -*-

from typing import Optional, List

from fastapi import APIRouter, status, Form, File, UploadFile, HTTPException
from pydantic import BaseModel, EmailStr

# write in __init__.py
app04 = APIRouter()

# https://www.imooc.com/video/22992  4-4 0:00


"""Response Model 响应模型"""


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    mobile: str = "10086"
    address: str = None
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr  # 用 EmailStr 需要 pip install pydantic[email]
    mobile: str = "10086"
    address: str = None
    full_name: Optional[str] = None


users = {
    "user01": {"username": "user01", "password": "123123", "email": "user01@example.com"},
    "user02": {"username": "user02", "password": "123456", "email": "user02@example.com", "mobile": "110"}
}


@app04.post("/response_model/", response_model=UserOut, response_model_exclude_unset=True)
async def response_model(user: UserIn):
    """response_model_exclude_unset=True表示默认值不包含在响应中，仅包含实际给的值，如果实际给的值与默认值相同也会包含在响应中"""
    print(user.password)  # password不会被返回
    # return user
    return users["user01"]


@app04.post(
    "/response_model/attributes",
    response_model=UserOut,
    # response_model=Union[UserIn, UserOut],   # UserIn和UserOut中的字段取并集
    # response_model=List[UserOut],
    response_model_include=["username", "email", "mobile"],
    response_model_exclude=["mobile"]
)
async def response_model_attributes(user: UserIn):
    """response_model_include列出需要在返回结果中包含的字段；response_model_exclude列出需要在返回结果中排除的字段"""
    # del user.password  # Union[UserIn, UserOut]后，删除password属性也能返回成功
    return user
    # return [user, user]

"""Response Status Code 响应状态码"""


@app04.post("/status_code", status_code=200)
async def status_code():
    return {"status_code": 200}


@app04.post("/status_attribute", status_code=status.HTTP_200_OK)
async def status_attribute():
    print(type(status.HTTP_200_OK))
    return {"status_code": status.HTTP_200_OK}

"""Form Data 表单数据处理"""


@app04.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):  # 定义表单参数
    """用Form类需要pip install python-multipart; Form类的元数据和校验方法类似Body/Query/Path/Cookie"""
    return {"username": username}
