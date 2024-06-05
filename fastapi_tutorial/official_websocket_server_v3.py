# -*- coding: utf-8 -*-
"""
https://fastapi.tiangolo.com/zh/advanced/websockets/
pip install websockets -i https://pypi.tuna.tsinghua.edu.cn/simple

bili_video: https://www.bilibili.com/video/BV1444y1Q74k/

https://fastapi.tiangolo.com/zh/advanced/websockets/#_4
注意不同python3.x版本的依赖导入有区别

认真理解，这个就是最基本的多人聊天Demo了
"""

"""
您也可以使用 from starlette.websockets import WebSocket。
FastAPI 直接提供了相同的 WebSocket，只是为了方便开发人员。但它直接来自 Starlette。
所以，更多Websocket的应用可以看：
https://www.starlette.io/websockets/
https://www.starlette.io/endpoints/#websocketendpoint
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

import uvicorn

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat Websocket Demo V3</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
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


"""
当 WebSocket 连接关闭时，await websocket.receive_text() 将引发 WebSocketDisconnect 异常，您可以捕获并处理该异常，就像本示例中的示例一样。
"""

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

# run method 1:
# uvicorn official_websocket_server:app --reload

"""
Test:
尝试以下操作：

使用多个浏览器选项卡打开应用程序。
从这些选项卡中发送消息。
然后关闭其中一个选项卡。
这将引发 WebSocketDisconnect 异常，并且所有其他客户端都会收到类似以下的消息：

Client #1596980209979 left the chat
"""

# todo learn use postman to test websocket api

if __name__ == '__main__':
    # swagger doc update need stop and start
    # cmd启动命令:
    # uvicorn run:app --host <api_ip> --port <api_port> --reload --workers 2
    # 程序启动方式
    uvicorn.run('official_websocket_server_v3:app', host='0.0.0.0', port=8000, reload=True, workers=2)
