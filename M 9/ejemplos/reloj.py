from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import datetime
import asyncio

app = FastAPI()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Hola mundo</title>
    </head>
    <body>
        <h1>Hola mundo!</h1>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var server_message = event.data;
                document.body.innerHTML = '<h1>' + server_message + '</h1>';
            };
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
        now = datetime.datetime.now().strftime("%I:%M:%S %p")
        await websocket.send_text(f"La hora es: {now}")
        await asyncio.sleep(1)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

