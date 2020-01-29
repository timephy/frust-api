from functools import reduce

import db
from server import sio, emit_message
import utils


# CONSTANTS

HOURS_LIMIT = 24 * 7  # every hour of a week


# VARIABLES

user_count = 0
users = {}

click_count_total = 0
event_count_total = 0
click_count_hour = 0
event_count_hour = 0

click_count_today = 0
event_count_today = 0

# USER EVENTS


async def user_connect(sid):
    # cache
    global user_count
    user_count += 1

    users[sid] = {
        "name": None,
        "click_count_session": 0,
        "event_count_session": 0
    }

    # send initial stats to new client
    await sio.emit("stats", get_stats(), room=sid)
    # send new status to clients
    await sio.emit("status", get_status())


async def user_disconnect(sid):
    # cache
    global user_count
    user_count -= 1

    await user_auth(sid, name=None)
    del users[sid]

    # send new status to clients
    await sio.emit("status", get_status())


async def user_auth(sid, *, name):
    # cache
    old_name = users[sid]["name"] if sid in users else None

    if name != old_name:  # join, leave, rename
        # set new name
        users[sid]["name"] = name
        # send message to users
        if name is not None and old_name is None:  # join
            text = f"{name} ist beigetreten."
        elif name is None and old_name is not None:  # leave
            text = f"{old_name} hat verlassen."
        else:  # rename
            text = f"{old_name} hat sich umbenannt zu {name}."
        await emit_message(text)


async def user_click(sid, *, user, comment, style):
    # cache
    await user_auth(sid, name=user)

    global click_count_total, click_count_today, click_count_hour
    click_count_total += 1
    click_count_today += 1
    click_count_hour += 1

    users[sid]["click_count_session"] += 1

    # click
    click = db.add_click(user=user, comment=comment, style=style)

    # user

    click_count_session = users[sid]["click_count_session"]
    if click_count_session != 0 and (click_count_session % 100 == 0
                                     or click_count_session == 50):
        await emit_message(f"{user} erreicht {click_count_session} Klicks!")
    await sio.emit("click", click)


async def user_event(sid, *, user, name):
    # cache
    await user_auth(sid, name=user)

    global event_count_total, event_count_today, event_count_hour
    event_count_total += 1
    event_count_today += 1
    event_count_hour += 1

    users[sid]["event_count_session"] += 1

    # event
    event = db.add_event(user=user, name=name)

    # user

    await emit_message(f"{user} triggered {name}!")
    await sio.emit("event", event)


# REQUESTS

get_clicks = db.get_clicks
get_events = db.get_events
get_users = db.get_users


def get_hours(since):
    list = db.get_hours(since=since)
    if utils.time() >= since:
        list.append({
            "timestamp": utils.time_hour(),
            "click_count": click_count_hour,
            "event_count": event_count_hour,
            "click_count_total": click_count_total,
            "event_count_total": event_count_total
        })
    return list


def get_online_users():
    return list(users.values())


def get_stats():
    return {
        "click_count_total": click_count_total,
        "click_count_today": click_count_today,
        "click_count_hour": click_count_hour,
        "event_count_total": event_count_total,
        "event_count_today": event_count_today,
        "event_count_hour": event_count_hour
    }


def get_status():
    return {
        "user_count": user_count
    }


# TASKS

async def start_hour(timestamp):
    global click_count_total, click_count_hour, click_count_today
    global event_count_total, event_count_hour, event_count_today

    # today
    hours = db.get_hours(since=utils.time_day())
    click_count_today = reduce(lambda val, hour: val + hour["click_count"],
                               hours, 0)
    event_count_today = reduce(lambda val, hour: val + hour["event_count"],
                               hours, 0)

    # total, hour
    hour = db.get_hour(timestamp)
    click_count_hour = hour["click_count"]
    event_count_hour = hour["event_count"]
    click_count_total = hour["click_count_total"]
    event_count_total = hour["event_count_total"]

    await sio.emit("stats", get_stats())


async def end_hour(timestamp):
    db.set_hour(timestamp=timestamp,
                clicks=click_count_hour,
                events=event_count_hour,
                clicks_total=click_count_total,
                events_total=event_count_total)


# INIT
