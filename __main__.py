import asyncio
import sys
import logging
import datetime

from aiohttp import web

from server import app, sio
import data
import utils


VERSION = "1.0"


# HTTP ROUTES

routes = web.RouteTableDef()


@routes.get("/api")
@utils.return_to_json
def index(request):
    return {"version": VERSION}


@routes.get("/api/latest_clicks")
@utils.return_to_json
def latest_clicks(request):
    return data.get_clicks(since=utils.time_day())


@routes.get("/api/latest_events")
@utils.return_to_json
def latest_events(request):
    return data.get_events(since=utils.time_day())


@routes.get("/api/latest_hours")
@utils.return_to_json
def latest_hours(request):
    week_ago = utils.time_day() - utils.SECS_PER_DAY * 6
    return data.get_hours(since=week_ago)


@routes.get("/api/users")
@utils.return_to_json
def users(request):
    return data.get_users()


@routes.get("/api/online_users")
@utils.return_to_json
def online_users(request):
    return data.get_online_users()


@routes.get("/api/current_stats")
@utils.return_to_json
def current_stats(request):
    return data.get_stats()


# SOCKET.IO EVENTS

@sio.event
@utils.sio_catch_error
async def click(sid, sent_data):
    print(f"click({sid}, {sent_data})")

    user, comment, style = utils.extract_click_data(sent_data)
    await data.user_click(sid, user=user, comment=comment, style=style)


@sio.event
@utils.sio_catch_error
async def event(sid, sent_data):
    print(f"event({sid}, {sent_data})")

    user, name = utils.extract_event_data(sent_data)
    await data.user_event(sid, user=user, name=name)


@sio.event
async def auth(sid, sent_data):
    print(f"auth({sid}, {sent_data})")

    name = utils.extract_name(sent_data)
    await data.user_auth(sid, name=name)


@sio.event
async def connect(sid, environ):
    print(f"connect({sid})")  # ", {environ})")
    await data.user_connect(sid)


@sio.event
async def disconnect(sid):
    print(f"disconnect({sid})")
    await data.user_disconnect(sid)


@sio.event
async def connect_error():
    print("A Socket.io connection failed!")


# TASKS

async def hourly_task():
    while True:
        # sleep until next hour
        current_time = utils.time()
        current_secs = current_time % utils.SECS_PER_HOUR
        remaining_secs = utils.SECS_PER_HOUR - current_secs
        logging.debug(
            f"[{datetime.datetime.now()}] hourly_task sleeping for "
            f"{remaining_secs} seconds")
        await asyncio.sleep(remaining_secs)

        # do stuff
        data.next_hour()


# SETUP TASKS

async def start_background_tasks(app):
    app["hourly_task"] = asyncio.create_task(hourly_task(), name="hourly_task")


async def cleanup_background_tasks(app):
    app["hourly_task"].cancel()
    await app["hourly_task"]

app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)


# RUN APP

# set routes of app
app.router.add_routes(routes)

# dev mode
if "--dev" in sys.argv:
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Developer mode (serving static content)")

    # Redirect / to /index.html (/ does not work)
    app.router.add_get("/", lambda _: web.HTTPFound('/index.html'))

    # Serve static content (order is important: files always last)
    app.add_routes([
        web.get("/version", lambda _: utils.dumps({
            "commit_sha": "dev",
            "timestamp": utils.time_day()
        }))
    ])
    app.router.add_static("/", "./frontend")

web.run_app(app, port=80)
