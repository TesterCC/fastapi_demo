# -*- coding: utf-8 -*-
'''
https://fastapi.tiangolo.com/zh/advanced/websockets/
pip install websockets -i https://pypi.tuna.tsinghua.edu.cn/simple

bili_video: https://www.bilibili.com/video/BV1444y1Q74k/
'''


'''
您也可以使用 from starlette.websockets import WebSocket。
FastAPI 直接提供了相同的 WebSocket，只是为了方便开发人员。但它直接来自 Starlette。
'''

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI Websocket Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
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


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # 使用 await 等待消息并发送消息
        await websocket.send_text(f"Message text was: {data}")

# run method 1:
# uvicorn official_websocket_server:app --reload

if __name__ == '__main__':
    # swagger doc update need stop and start
    # cmd启动命令:
    # uvicorn run:app --host <api_ip> --port <api_port> --reload --workers 2
    # 程序启动方式
    uvicorn.run('official_websocket_server:app', host='0.0.0.0', port=8000, reload=True, workers=2)
