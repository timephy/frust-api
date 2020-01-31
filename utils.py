import ujson
import functools
import time as _time

from aiohttp import web


# CONSTANTS

SECS_PER_HOUR = 60 * 60
SECS_PER_DAY = SECS_PER_HOUR * 24
SECS_PER_WEEK = SECS_PER_DAY * 7


# INPUT PARSING

def sanitize_str(str):
    """Strip input and if empty return None."""
    str = str.strip()
    if str == "":
        return None
    return str


def extract_name(data):
    name = sanitize_str(data)

    if type(name) is not str:
        raise Exception("data must be of type String")

    return name


def extract_click_data(data):
    # get values, get() defaults to None
    user = sanitize_str(data.get("user"))
    comment = sanitize_str(data.get("comment"))
    style = sanitize_str(data.get("style"))

    # check types
    if not user or type(user) is not str:
        raise Exception("user must be of type String")
    if comment and type(comment) is not str:
        raise Exception("comment is not of type String?")
    if style and type(style) is not str:
        raise Exception("style is not of type String?")

    return user, comment, style


def extract_event_data(data):
    # get values, get() defaults to None
    user = sanitize_str(data.get("user"))
    name = sanitize_str(data.get("name"))

    # check types
    if not user or type(user) is not str:
        raise Exception("user must be of type String")
    if not name or type(name) is not str:
        raise Exception("name must be of type String")

    return user, name


# MISC

def dumps(data):
    """json.dumps with indent of 2."""
    return web.Response(text=ujson.dumps(data, indent=2))


def return_to_json(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return dumps(func(*args, **kwargs))
    return wrapper


def sio_catch_error(func):
    @functools.wraps(func)
    async def wrapper(sid, data):
        try:
            return await func(sid, data)
        except Exception as e:
            raise e
            print(f"{sid} sent invalid data (to {func.__name__}):", e)
    return wrapper


# TIME

def time():
    """Current time."""
    return int(_time.time())


def time_hour(current_time=None):
    """The time the current hour began."""
    if current_time is None:
        current_time = time()
    return current_time - current_time % SECS_PER_HOUR


def time_day(current_time=None):
    """The time the current day began."""
    if current_time is None:
        current_time = time()
    return current_time - current_time % SECS_PER_DAY
