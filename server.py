from aiohttp import web
import socketio


# SETUP WEB SERVER

app = web.Application()

sio = socketio.AsyncServer(async_mode="aiohttp")
sio.attach(app, socketio_path="/api/socket.io")


async def emit_message(text, *, style="medium highlight", type="toast"):
    await sio.emit("message", {
        "text": text,
        "style": style,
        "type": type
    })
