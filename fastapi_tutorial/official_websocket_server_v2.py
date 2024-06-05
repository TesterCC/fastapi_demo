# -*- coding: utf-8 -*-
"""
https://fastapi.tiangolo.com/zh/advanced/websockets/
pip install websockets -i https://pypi.tuna.tsinghua.edu.cn/simple

bili_video: https://www.bilibili.com/video/BV1444y1Q74k/

https://fastapi.tiangolo.com/zh/advanced/websockets/#depends
注意不同python3.x版本的依赖导入有区别
"""

"""
您也可以使用 from starlette.websockets import WebSocket。
FastAPI 直接提供了相同的 WebSocket，只是为了方便开发人员。但它直接来自 Starlette。
"""

# 注意不同python3.x版本的依赖导入有区别
from typing import Annotated

"""
在 WebSocket 端点中，您可以从 fastapi 导入并使用以下内容：

Depends
Security
Cookie
Header
Path
Query
它们的工作方式与其他 FastAPI 端点/ 路径操作 相同
"""

from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketException,
    status,
)
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat V2</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var itemId = document.getElementById("itemId")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost:8000/items/" + itemId.value + "/ws?token=" + token.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


async def get_cookie_or_token(
        websocket: WebSocket,
        session: Annotated[str | None, Cookie()] = None,
        token: Annotated[str | None, Query()] = None,
):
    if session is None and token is None:
        # 由于这是一个 WebSocket，抛出 HTTPException 并不是很合理，而是抛出 WebSocketException。
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@app.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
        *,
        websocket: WebSocket,
        item_id: str,
        q: int | None = None,
        cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(
            f"Session cookie or query token value is: {cookie_or_token}"
        )
        if q is not None:
            await websocket.send_text(f"Query parameter q is: {q}")
        await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")


# run method 1:
# uvicorn official_websocket_server:app --reload

if __name__ == '__main__':
    # swagger doc update need stop and start
    # cmd启动命令:
    # uvicorn run:app --host <api_ip> --port <api_port> --reload --workers 2
    # 程序启动方式
    uvicorn.run('official_websocket_server_v2:app', host='0.0.0.0', port=8000, reload=True, workers=2)
