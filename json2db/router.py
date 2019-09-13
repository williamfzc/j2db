from fastapi import Form, FastAPI
import typing

from json2db.models import JsonRequestModel, EventModel


def register(app: FastAPI, handler: typing.Callable):
    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    @app.post("/api/json/form")
    def json_upload_form(
        *, table: str = Form(...), action: str = Form(...), content: str = Form(...)
    ):
        new_event = EventModel(table, action, content)
        return handler(new_event)

    @app.post("/api/json/raw")
    def json_upload_raw(*, request: JsonRequestModel):
        new_event = EventModel(request.table, request.action, request.content)
        return handler(new_event)
