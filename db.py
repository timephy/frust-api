from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db_model import Base, Click, User, Hour, Event  # Stats
import utils

engine = create_engine("sqlite:///db.sqlite")
Base.metadata.create_all(engine)
connection = engine.connect()


# UTILS

def transactional(func):
    def wrapper(*args, **kwargs):
        if len(args) > 0 and isinstance(args[0], Session):
            # if session is given, just run function
            session = args.pop(0)
            return func(session, *args, **kwargs)
        else:
            # if session is not given, create one, run function,
            # then try to commit it
            session = Session(bind=connection)
            val = func(session, *args, **kwargs)
            try:
                session.commit()
                return val
            except:
                session.rollback()
                raise
            finally:
                session.close()
    return wrapper


# Stats.to_json = lambda stats: {
#     "click_count_total": stats.total,
#     "click_count_today": stats.today,
#     "click_count_hour": stats.hour,
#     "user_count": 0
# }


Click.to_json = lambda click: {
    "user": click.user,
    "comment": click.comment,
    "style": click.style,
    "timestamp": click.timestamp
}

Event.to_json = lambda event: {
    "user": event.user,
    "name": event.name,
    "timestamp": event.timestamp
}

Hour.to_json = lambda hour: {
    "timestamp": hour.timestamp,
    "click_count": hour.clicks,
    "event_count": hour.events,
    "click_count_total": hour.clicks_total,
    "event_count_total": hour.events_total
}

User.to_json = lambda user: {
    "name": user.name,
    "click_count": user.clicks,
    "event_count": user.events
}


def _user(session, name):
    obj = session.query(User).get(name)
    if obj is None:
        obj = User(name=name, clicks=0, events=0)
        session.add(obj)
    return obj


# def _hour(session, timestamp):
#     obj = session.query(Hour).get(timestamp)
#     if obj is None:
#         obj = Hour(timestamp=timestamp,
#                    clicks=0, events=0,
#                    clicks_total=0, events_total=0)
#         session.add(obj)
#     return obj


#

@transactional
def add_click(session, *, user, comment, style):
    click = Click(user=user, comment=comment,
                  style=style, timestamp=utils.time())
    session.add(click)

    user = _user(session, user)
    user.clicks += 1

    return click.to_json()


@transactional
def add_event(session, *, user, name):
    event = Event(user=user, name=name, timestamp=utils.time())
    session.add(event)

    user = _user(session, user)
    user.events += 1

    return event.to_json()


# @transactional
# def inc_user_clicks(session, *, user_name):
#     user = _user(session, user_name)
#     user.clicks += 1


# @transactional
# def inc_user_events(session, *, user_name):
#     user = _user(session, user_name)
#     user.events += 1


#

@transactional
def get_clicks(session, *, since):
    return [click.to_json() for click in session.query(Click)
            .order_by(Click.id.desc())
            .filter(Click.timestamp >= since)]


@transactional
def get_events(session, *, since):
    return [event.to_json() for event in session.query(Event)
            .order_by(Event.id.desc())
            .filter(Event.timestamp >= since)]


@transactional
def get_hours(session, *, since):
    return [hour.to_json() for hour in session.query(Hour)
            .order_by(Hour.timestamp.desc())
            .filter(Hour.timestamp >= since)]


@transactional
def get_users(session):
    return [user.to_json() for user in session.query(User).all()]


@transactional
def get_hour(session, timestamp):
    hour = session.query(Hour).order_by(Hour.timestamp.desc()).first()
    if hour is None:
        return {
            "timestamp": utils.time_hour(),
            "click_count": 0,
            "event_count": 0,
            "click_count_total": 0,
            "event_count_total": 0
        }
    obj = hour.to_json()
    if hour.timestamp == timestamp:
        session.delete(hour)  # because this hour is kept in cache
    else:
        obj["click_count"] = 0
        obj["event_count"] = 0
    return obj


@transactional
def set_hour(session, timestamp, *,
             clicks, events, clicks_total, events_total):
    hour = session.query(Hour).get(timestamp)
    if hour is None:
        hour = Hour(timestamp=timestamp)
        session.add(hour)
    hour.clicks = clicks
    hour.events = events
    hour.clicks_total = clicks_total
    hour.events_total = events_total
