import sqlite3
import datetime


async def add_click(name: str, comment: str):
    """Stores a click to the database and returns this click object (dict)."""
    click = {"date": 123456789, "name": name, "comment": comment}
    # db.store(click)
    return click


async def get_last_clicks(count: int = 1000):
    """Returns last `count` clicks from the database."""
    # return db.last(count)
    return [{"date": 123456789, "name": "Name", "comment": "Comment"}] * 5


async def get_total_clicks():
    """Returns the total amout of clicks."""
    return 900


async def get_day_clicks():
    """Returns the amout of clicks today."""
    return 500


async def get_hour_clicks():
    """Returns the amout of clicks in the last hour."""
    return 100


async def get_stats():
    return {
        "total": await get_total_clicks(),
        "day": await get_day_clicks(),
        "hour": await get_hour_clicks()
    }
