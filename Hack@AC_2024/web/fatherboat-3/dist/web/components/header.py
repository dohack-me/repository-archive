from nicegui import app, ui

def header() -> None:
    """
    Default sticky header
    """

    with ui.header(elevated=True).style("background-color: rgb(85, 214, 244)").classes("justify-between"):
        ui.label("Fatherboat 3.0").classes("text-4xl font-bold text-blue-grey-7")
        with ui.row():
            ui.button("Posts", icon="feed", on_click=lambda: ui.open("/")).props("flat color=blue-grey-7")
            ui.button("Create", icon="add", on_click=lambda: ui.open("/submit")).props("flat color=blue-grey-7")
            if app.storage.user.get("id", False):
                ui.button("Logout", icon="logout", on_click=logout).props("flat color=blue-grey-7")
            else:
                ui.button("Login", icon="login", on_click=lambda: ui.open("/login")).props("flat color=blue-grey-7")

def logout():
    app.storage.user.clear()
    ui.run_javascript("location.reload()")
