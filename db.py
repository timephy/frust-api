import sqlite3
import datetime


current_total_clicks = 45000
current_day_clicks = 43500


async def add_click(name: str, comment: str, style: str):
    """Stores a click to the database and returns this click object (dict)."""
    click = {
        "timestamp": 123456789,
        "name": name,
        "comment": comment,
        "style": style
    }
    global current_total_clicks
    global current_day_clicks
    current_total_clicks += 1
    current_day_clicks += 1
    # db.store(click)
    return click


async def get_last_clicks(count: int = 1000):
    """Returns last `count` clicks from the database."""
    # return db.last(count)
    return [{"date": 123456789, "name": "Name", "comment": "Comment"}] * 5


async def get_total_clicks():
    """Returns the total amout of clicks."""
    global current_total_clicks
    return current_total_clicks


async def get_day_clicks():
    """Returns the amout of clicks today."""
    global current_day_clicks
    return current_day_clicks


async def get_stats():
    # TODO: await together
    return {
        "total": await get_total_clicks(),
        "day": await get_day_clicks()
    }
