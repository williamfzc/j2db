from fastapi import FastAPI
import uvicorn
from loguru import logger

from j2db import constants
from j2db import router
from j2db import __PROJECT_NAME__, __VERSION__
from j2db.db import BaseManager, BaseModel
from j2db.handler import EventHandler

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
        logger.info(f"using: {__PROJECT_NAME__} ver {__VERSION__}")

        # db has not default value
        assert self.db_manager, "init db first"
        # if custom handler existed
        if not self.handler:
            self.handler = EventHandler(self.db_manager)
        # register
        router.register(app, self.handler)
        uvicorn.run(
            app, host="0.0.0.0", port=self.port, log_level=constants.SERVER_LOG_LEVEL
        )
