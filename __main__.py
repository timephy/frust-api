# import gevent.pywsgi
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.wsgi import responder
from werkzeug.exceptions import NotFound, HTTPException
import wsgiref.simple_server
import json
import static_content
import functools
from geventwebsocket import WebSocketApplication


PORT = 80

# werkzeug object
map = Map([])
# '/api' route return list
api_paths = []


class HTTP_Method:
    GET = ("GET",)
    POST = ("POST",)


def KeyErrorToNotFound(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            raise NotFound
    return wrapper


def route(url_path, http_methods=HTTP_Method.GET, desc=None):
    """
    Decorator for a function that with signature (req, values).

    Registers function to be called when a HTTP request for 'url_path' is
    handled. The return value is sent to the client.
    """
    if not isinstance(url_path, str):
        raise Exception("'url_path' has to be of type 'str'.")

    def decorator(func):
        # register function to url-path
        print(url_path, "->", func.__name__,
              f"""[{", ".join(http_methods)}]""")
        r = Rule(url_path, endpoint=func, methods=http_methods)
        map.add(r)
        map.update()
        path = {
            "path": url_path,
            "methods": list(http_methods)
        }
        if desc:
            path["description"] = desc
        api_paths.append(path)

        # return function, no wrapper
        return func
    return decorator


@responder
def handle(environ, start_response):
    try:
        # Wrapper objects
        req = Request(environ)

        # Match URL to endpoint (function)
        adapter = map.bind_to_environ(environ)
        endpoint, values = adapter.match()  # values not used

        return endpoint(req, values)
    except NotFound:
        return Response(static_content.html_files["404.html"],
                        mimetype="text/html",
                        status=404)
    except HTTPException as e:
        return e
    except Exception as e:
        # Normal exceptions should never happen, raise to print
        raise e


# Open websockets to send updates to
sockets = []


class ClickApplication(WebSocketApplication):
    def on_open(self):
        sockets.append(self)

    def on_message(self, message):
        for socket in sockets:
            socket.ws.send(message)

    def on_close(self, reason):
        sockets.remove(self)


# API


@route("/api/status")
def status(req, values):
    pass


@route("/api/history")
def history(req, values):
    pass


@route("/ws")
def ws(req, values):
    pass


# Static content


@route("/")
def root(req, values):
    return html(req, {"file": "index.html"})


@route("/<file>")
@KeyErrorToNotFound
def html(req, values):
    return Response(static_content.html_files[values["file"]],
                    mimetype="text/html")


@route("/scripts/<file>")
@KeyErrorToNotFound
def js(req, values):
    return Response(static_content.js_files[values["file"]],
                    mimetype="text/javascript")


@route("/styles/<file>")
@KeyErrorToNotFound
def css(req, values):
    return Response(static_content.css_files[values["file"]],
                    mimetype="text/css")


@route("/images/<file>")
@KeyErrorToNotFound
def img(req, values):
    return Response(static_content.img_files[values["file"]],
                    mimetype="image")


# Start server
with wsgiref.simple_server.make_server("", PORT, handle) as httpd:
    print(f"Serving on port {PORT}...")
    httpd.serve_forever()
