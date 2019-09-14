import typing
from loguru import logger

from j2db import errors
from j2db.db import BaseManager
from j2db import toolbox
from j2db.models import EventModel


class EventHandler(object):
    def __init__(self, db_manager: BaseManager):
        self.db_manager = db_manager

    def before(self, event: EventModel):
        """ hook. will execute before handle """
        return event

    def handle(self, event: EventModel) -> typing.Dict:
        logger.info(f"event received: {event}")
        event = self.before(event)

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
        return {"status": "ok"}
