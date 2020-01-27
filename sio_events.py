from server import sio
import data
import utils


@sio.event
@utils.sio_catch_error
async def click(sid, sent_data):
    print(f"click({sid}, {sent_data})")

    user, comment, style = utils.extract_click_data(sent_data)
    await data.user_click(sid, user=user, comment=comment, style=style)


@sio.event
@utils.sio_catch_error
async def event(sid, sent_data):
    print(f"event({sid}, {sent_data})")

    user, name = utils.extract_event_data(sent_data)
    await data.user_event(sid, user=user, name=name)


@sio.event
async def auth(sid, sent_data):
    print(f"auth({sid}, {sent_data})")

    name = utils.extract_name(sent_data)
    await data.user_auth(sid, name=name)


@sio.event
async def connect(sid, environ):
    print(f"connect({sid})")  # ", {environ})")
    await data.user_connect(sid)


@sio.event
async def disconnect(sid):
    print(f"disconnect({sid})")
    await data.user_disconnect(sid)


@sio.event
async def connect_error():
    print("A Socket.io connection failed!")
