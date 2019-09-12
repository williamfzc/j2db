from fastapi import Form, FastAPI
import typing

from json2db.request import JsonRequest


def register(app: FastAPI, handler: typing.Callable):
    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    @app.post("/api/json/form")
    def json_upload_form(*, tag: str = Form(...), content: str = Form(...)):
        return handler(tag, content)

    @app.post("/api/json/params")
    def json_upload(*, request: JsonRequest):
        return handler(request.tag, request.content)
