from fastapi import FastAPI, Form
import uvicorn

from json2db import toolbox
from json2db import errors
from json2db import constants
from json2db.request import JsonRequest

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/json/form")
def json_upload_form(*, tag: str = Form(...), content: str = Form(...)):
    origin_request = {"tag": tag, "content": content}
    # format check
    if not toolbox.is_json_valid(content):
        return errors.JsonInvalidError(origin_request)
    return origin_request


@app.post("/api/json/params")
def json_upload(*, request: JsonRequest):
    # format check
    if not toolbox.is_json_valid(request.content):
        return errors.JsonInvalidError(request)
    return request


def start_server(port: int = None):
    if not port:
        port = constants.PORT

    uvicorn.run(app, host="0.0.0.0", port=port, log_level=constants.SERVER_LOG_LEVEL)


if __name__ == "__main__":
    start_server()
