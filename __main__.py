import asyncio
from aiohttp import web
import socketio
import json

sio = socketio.AsyncServer(async_mode="aiohttp")

app = web.Application()
sio.attach(app)

# A counter for the connected socket.io client
client_counter = 0


def pretty_json_response(data):
    return web.Response(text=json.dumps(data, indent=2))


# HTTP Routes
async def index(request):
    return pretty_json_response({
        "version": "0.1"
    })


async def history(request):
    return pretty_json_response([
        {"time": 1234567, "name": "Name here", "comment": "Comment here"}
    ] * 5)


# set routes of app
app.add_routes([
    web.get("/api", index),
    web.get("/api/history", history)
])

# Socket.io Events


@sio.event
async def clicked(sid, data):
    print(f"clicked({sid}, {data})")

    await sio.emit("clicked", data)


@sio.event
async def connect(sid, environ):
    print(f"connect({sid})")  # ", {environ})")

    global client_counter
    client_counter += 1
    await sio.emit("stats", {"total": 90, "day": 50, "hour": 10}, room=sid)
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
