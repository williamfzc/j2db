from fastapi import FastAPI
import uvicorn

from json2db import constants
from json2db import router
from json2db.db import BaseManager, BaseModel
from json2db.handler import EventHandler

app = FastAPI()


class Server(object):
    def __init__(
            self,
            port: int = None,
            db_manager: BaseManager = None,
            handler: EventHandler = None,
    ):
        if not port:
            port = constants.PORT
        self.port: int = port
        self.db_manager: BaseManager = db_manager
        self.handler: EventHandler = handler

    def init_db(self, db: BaseManager, create_tables: bool = None):
        self.db_manager = db

        if create_tables:
            BaseModel.metadata.create_all(self.db_manager.engine)

    def start(self):
        # db has not default value
        assert self.db_manager, "init db first"
        # handler has
        if not self.handler:
            self.handler = EventHandler(self.db_manager)
        # register
        router.register(app, self.handler)
        uvicorn.run(
            app, host="0.0.0.0", port=self.port, log_level=constants.SERVER_LOG_LEVEL
        )
