from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import Client, app, ui
import secrets

import edgedb
from components import header
from generated_edgeql import authenticate_user, create_post, create_user, get_posts

from util import sanitize_url, visit_url

SECRET = secrets.token_hex(64)

EDGEDB_URL = "edgedb://db:5656?edgedb"

if EDGEDB_URL == "":
    db = edgedb.create_client(timeout=10000)
else:
    db = edgedb.create_client(dsn=EDGEDB_URL, timeout=10000)


unrestricted_page_routes = {"/login", "/register"}


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get("id", False):
            if request.url.path in Client.page_routes.values() and request.url.path not in unrestricted_page_routes:
                app.storage.user["referrer_path"] = request.url.path  # remember where the user wanted to go
                return RedirectResponse("/login")
        return await call_next(request)


app.add_middleware(AuthMiddleware)


@ui.page("/")
async def index():
    user_db = db.with_globals({"current_user_id": app.storage.user.get("id")})
    posts = get_posts(user_db)

    header()
    if len(posts) == 0:
        ui.label("No posts yet").classes("self-center text-xl font-bold")
    else:
        for post in posts:
            with ui.card():
                ui.label(post.title).classes("text-xl font-bold")
                ui.label(post.body.decode())


@ui.page("/login")
async def login():
    header()
    with ui.element("div").classes("w-80 self-center"):
        username = ui.input(label="Username")
        password = ui.input(label="Password", password=True, password_toggle_button=True)

        with ui.element("div").classes("flex mt-4 justify-between items-center"):
            ui.link("Register", "/register")
            ui.button("Login", on_click=lambda: login__INTERNAL(username.value, password.value))


@ui.page("/register")
async def register():
    header()
    with ui.element("div").classes("w-80 self-center"):
        username = ui.input(label="Username")
        password = ui.input(label="Password", password=True, password_toggle_button=True)

        with ui.element("div").classes("flex mt-4 justify-between items-center"):
            ui.link("Login", "/login")
            ui.button("Register", on_click=lambda: register__INTERNAL(username.value, password.value))


@ui.page("/submit")
async def submit():
    header()
    with ui.element("div").classes("w-80 self-center"):
        title = ui.input(label="Title")
        url = ui.input(label="URL")

        with ui.element("div").classes("flex mt-4 justify-between items-center"):
            ui.button("Submit", on_click=lambda: createPost__INTERNAL(title.value, url.value))


def login__INTERNAL(
    username: str,
    password: str,
):
    if user := authenticate_user(db, username=username, password=password):
        app.storage.user["id"] = str(user.id)
        ui.open("/")
        return {"success": True, "message": "Successfully logged in"}
    else:
        ui.notify("Invalid credentials", type="negative")
        return {"success": False, "message": "Invalid credentials"}


def register__INTERNAL(
    username: str,
    password: str,
):
    try:
        create_user(db, username=username, password=password)
    except Exception as e:
        ui.notify(str(e), type="negative")
        return {"success": False, "message": str(e)}
    ui.open("/login")
    return {"success": True, "message": "Successfully registered"}


def createPost__INTERNAL(title: str, url: str):
    author_id = app.storage.user.get("id", False)
    if not author_id:
        return {"success": False, "message": "You are not logged in"}

    user_db = db.with_globals({"current_user_id": author_id})

    if title is None:
        ui.notify("Invalid title", type="negative")
        return {"success": False, "message": "Invalid title"}

    if not sanitize_url(url):
        ui.notify("Invalid url", type="negative")
        return {"success": False, "message": "Invalid url"}
    else:
        try:
            content = visit_url(url)
            create_post(user_db, title=title, body=content, author_id=author_id)
        except Exception as e:
            ui.notify(str(e), type="negative")
            return {"success": False, "message": str(e)}
        ui.notify("Post created", type="positive")
        return {"success": True, "message": "Post created"}


ui.run(storage_secret=SECRET)
