from aiohttp import web
import json

import functools


def extract_click_data(data):
    if "name" not in data or type(data["name"]) is not str:
        raise Exception("name must be of type String")
    if "comment" in data and type(data["comment"]) is not str:
        raise Exception("comment is not of type String?")
    if "style" in data and type(data["style"]) is not str:
        raise Exception("style is not of type String?")
    # get() defaults to None
    return data["name"], data.get("comment"), data.get("style")


def extract_event_data(data):
    if "id" not in data or type(data["id"]) is not str:
        raise Exception("id must be of type String")
    return data["id"]


def dumps(data):
    """json.dumps with indent of 2"""
    return web.Response(text=json.dumps(data, indent=2))


def sio_catch_error(func):
    @functools.wraps(func)
    async def wrapper(sid, data):
        try:
            return await func(sid, data)
        except Exception as e:
            print(f"{sid} sent invalid data (to {func.__name__}):", e)
    return wrapper
