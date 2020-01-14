import asyncio
from aiohttp import web
import socketio
import sys

import db
import utils

VERSION = "0.1"

# Setup web server
sio = socketio.AsyncServer(async_mode="aiohttp")

app = web.Application()
sio.attach(app, socketio_path="/api/socket.io")


# A counter for the connected socket.io client
client_counter = 0
client_ids = []
client_names = {}
client_session_clicks = {}


# HTTP Routes
async def index(request):
    return utils.dumps({"version": VERSION})


async def history(request):
    return utils.dumps(await db.get_last_clicks())


async def list_current_users(request):
    return utils.dumps({
        "userCount": client_counter,
        "identifiedUsers": [{
            "name": client_names.get(sid, None),
            "sessionClicks": client_session_clicks.get(sid, 0)
        } for sid in client_ids]
    })


# Socket.io Events
@sio.event
@utils.sio_catch_error
async def click(sid, data):
    print(f"click({sid}, {data})")

    global client_session_clicks
    client_session_clicks[sid] += 1

    name, comment, style = utils.extract_click_data(data)

    global client_names
    client_names[sid] = name

    click = await db.add_click(name, comment, style)
    await sio.emit("click", click)


@sio.event
@utils.sio_catch_error
async def event(sid, data):
    print(f"event({sid}, {data})")

    name, event_id = utils.extract_event_data(data)

    global client_names
    client_names[sid] = name

    await sio.emit("event", {"name": name, "id": event_id})


@sio.event
async def connect(sid, environ):
    print(f"connect({sid})")  # ", {environ})")

    global client_ids
    client_ids.append(sid)

    global client_session_clicks
    client_session_clicks[sid] = 0

    global client_counter
    client_counter += 1

    await sio.emit("stats", await db.get_stats(), room=sid)
    await sio.emit("users", {"count": client_counter})


@sio.event
async def disconnect(sid):
    print(f"disconnect({sid})")
    global client_ids
    client_ids.remove(sid)

    global client_counter
    client_counter -= 1

    global client_session_clicks
    del client_session_clicks[sid]

    global client_names
    if sid in client_names:  # if user did send name
        del client_names[sid]

    await sio.emit("users", {"count": client_counter})


@sio.event
async def connect_error():
    print("The connection failed!")

# set routes of app
app.add_routes([
    web.get("/api", index),
    web.get("/api/history", history),
    web.get("/api/list", list_current_users)
])

# serve frontend for development
# use /index.html (/ does not work)
if "--dev" in sys.argv:
    print("Developer mode activated (serving static content).")
    # Logging
    import logging
    logging.basicConfig(level=logging.DEBUG)
    # Redirect / to /index.html
    app.router.add_get("/", lambda _: web.HTTPFound('/index.html'))
    # Server static content

    app.add_routes([
        web.get("/version", lambda _: utils.dumps({
            "commit_sha": "dev",
            "timestamp": "timestamp"
        }))
    ])

    app.router.add_static("/", "./frontend")


# Run app
asyncio.run(web.run_app(app, port=80))
