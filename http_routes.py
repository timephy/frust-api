from aiohttp import web

import data
import utils


routes = web.RouteTableDef()


@routes.get("/api")
@utils.return_to_json
def index(request):
    return {"version": "1.0"}


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
