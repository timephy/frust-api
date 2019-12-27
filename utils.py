from aiohttp import web
import json


def extract_click_data(data):
    if "name" not in data or type(data["name"]) is not str:
        raise Exception("name must be of type String")
    if "comment" in data and type(data["comment"]) is not str:
        raise Exception("comment is not of type String?")
    return data["name"], data["comment"]


def dumps(data):
    """json.dumps with indent of 2"""
    return web.Response(text=json.dumps(data, indent=2))
