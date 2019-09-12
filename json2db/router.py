from fastapi import Form, FastAPI
import typing

from json2db.request import JsonRequest


def register(app: FastAPI, handler: typing.Callable):
    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    @app.post("/api/json/form")
    def json_upload_form(
        *, tag: str = Form(...), action: str = Form(...), content: str = Form(...)
    ):
        return handler(tag, action, content)

    @app.post("/api/json/raw")
    def json_upload_raw(*, request: JsonRequest):
        return handler(request.tag, request.action, request.content)
