from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from json2db import toolbox
from json2db import errors
from json2db import constants

app = FastAPI()


class JsonRequest(BaseModel):
    # for matching models
    tag: str = ''
    # json
    content: str = ''


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/json/")
def json_upload(request: JsonRequest):
    # format check
    if not toolbox.is_json_valid(request.content):
        return errors.JsonInvalidError(request)
    return request


def start_server(port: int = None):
    if not port:
        port = constants.PORT

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level=constants.SERVER_LOG_LEVEL,
    )


if __name__ == '__main__':
    start_server()
