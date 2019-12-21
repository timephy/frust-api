import sqlite3
import datetime


async def add_click(name: str, comment: str):
    click = {"date": 123456789, "name": name, "comment": comment}
    # db.store(click)
    return click


async def get_last_clicks(count: int = 1000):
    # return db.last(count)
    return [{"date": 123456789, "name": "Name", "comment": "Comment"}] * 5
