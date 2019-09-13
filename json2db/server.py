from fastapi import FastAPI
import uvicorn
import typing
from loguru import logger

from json2db import toolbox
from json2db import errors
from json2db import constants
from json2db import router
from json2db.db import BaseManager, BaseModel
from json2db.models import EventModel

app = FastAPI()


class Server(object):
    def __init__(self, port: int = None):
        if not port:
            port = constants.PORT
        self.port: int = port
        self.db_manager: typing.Optional[BaseManager] = None

    def handler(self, event: EventModel):
        logger.info(f"event received: {event}")

        # TODO re implement with hook
        # format check
        logger.debug("format check ...")
        if not event.is_content_valid():
            logger.warning("json invalid")
            return errors.JsonInvalidError(event)

        # table name check
        logger.debug("table name check ...")
        if event.table not in self.db_manager.models:
            return errors.TableInvalidError(event)
        model = self.db_manager.models[event.table]

        # operation
        content_dict = toolbox.json2dict(event.content)
        data = model(**content_dict)
        operate_result = self.db_manager.apply_action(event.action, data)
        # some error happened
        if operate_result:
            return errors.DBOperatorError(event, operate_result)

        # TODO
        return "ok"

    def init_db(self, db: BaseManager, create_tables: bool = None):
        self.db_manager = db

        if create_tables:
            BaseModel.metadata.create_all(self.db_manager.engine)

    def start(self):
        assert self.db_manager, "init db first"
        router.register(app, self.handler)
        uvicorn.run(
            app, host="0.0.0.0", port=self.port, log_level=constants.SERVER_LOG_LEVEL
        )
