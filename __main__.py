import asyncio
from aiohttp import web
import socketio
import json

import db
import utils

VERSION = "0.1"

sio = socketio.AsyncServer(async_mode="aiohttp")

app = web.Application()
sio.attach(app, socketio_path="/api/socket.io")

# A counter for the connected socket.io client
client_counter = 0


def pretty_json_response(data):
    return web.Response(text=json.dumps(data, indent=2))


# HTTP Routes
async def index(request):
    return pretty_json_response({
        "version": VERSION
    })


async def history(request):
    return pretty_json_response(await db.get_last_clicks())


# set routes of app
app.add_routes([
    web.get("/api", index),
    web.get("/api/history", history)
])

# Socket.io Events


@sio.event
async def clicked(sid, data):
    print(f"clicked({sid}, {data})")

    utils.assert_click_data(data)
    click = await db.add_click(data["name"], data["comment"])
    await sio.emit("clicked", click)


@sio.event
async def connect(sid, environ):
    print(f"connect({sid})")  # ", {environ})")

    global client_counter
    client_counter += 1
    await sio.emit("stats", await db.get_stats(), room=sid)
    await sio.emit("users", {"count": client_counter})


@sio.event
async def disconnect(sid):
    print(f"disconnect({sid})")

    global client_counter
    client_counter -= 1
    await sio.emit("users", {"count": client_counter})


@sio.event
async def connect_error():
    print("The connection failed!")


# Run app
asyncio.run(web.run_app(app, port=80))
