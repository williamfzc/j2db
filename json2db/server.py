from fastapi import FastAPI, Form
import uvicorn
from loguru import logger

from json2db import toolbox
from json2db import errors
from json2db import constants
from json2db.request import JsonRequest

app = FastAPI()


# --- router ---
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/json/form")
def json_upload_form(*, tag: str = Form(...), content: str = Form(...)):
    return handler(tag, content)


@app.post("/api/json/params")
def json_upload(*, request: JsonRequest):
    return handler(request.tag, request.content)


# --- router end ---

def handler(tag: str, content: str):
    logger.info(f'event received')
    logger.debug(f'tag: {tag}')
    logger.debug(f'content: {content}')

    # format check
    logger.debug('format check ...')
    if not toolbox.is_json_valid(content):
        logger.warning(f'json invalid')
        return errors.JsonInvalidError({
            'tag': tag,
            'content': content,
        })

    # TODO orm check
    logger.debug('orm check ...')

    # TODO write db
    logger.debug('try to write db ...')

    return 'ok'


def start_server(port: int = None):
    if not port:
        port = constants.PORT

    uvicorn.run(app, host="0.0.0.0", port=port, log_level=constants.SERVER_LOG_LEVEL)


if __name__ == "__main__":
    start_server()
