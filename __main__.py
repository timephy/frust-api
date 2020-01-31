import asyncio
import sys
import logging
import datetime

from aiohttp import web
import uvloop

from server import app
import data
import utils
from http_routes import routes
import sio_events


uvloop.install()


# TASKS

async def hourly_task():
    while True:
        current_time = utils.time()
        current_hour = utils.time_hour(current_time=current_time)
        next_hour = current_hour + utils.SECS_PER_HOUR

        await data.start_hour(timestamp=current_hour)

        # sleep until next hour
        remaining_secs = next_hour - current_time
        logging.debug(
            f"[{datetime.datetime.now()}] hourly_task sleeping for "
            f"{remaining_secs} seconds")
        await asyncio.sleep(remaining_secs)

        await data.end_hour(timestamp=current_hour)


# SETUP TASKS

async def start_background_tasks(app):
    app["hourly_task"] = asyncio.create_task(hourly_task(), name="hourly_task")


async def cleanup_background_tasks(app):
    await data.end_hour(timestamp=utils.time_hour())
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
    app.router.add_get("/version.json", lambda _: utils.dumps({
        "commit_sha": f"{utils.time()}",
        "timestamp": f"{utils.time()}"
    }))
    app.router.add_static("/", "./frontend")

web.run_app(app, port=80)
