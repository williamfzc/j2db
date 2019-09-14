from pydantic import BaseModel
import json

from json2db import toolbox


class JsonRequestModel(BaseModel):
    """ for parsing args of request only """

    # for matching models
    table: str = ""
    # action
    action: str = ""
    # json
    content: str = ""


class EventModel(object):
    """ all the requests should be converted to this type, and sent to handler """

    def __init__(self, table: str, action: str, content: str):
        self.table = table
        self.action = action
        self.content = content

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return json.dumps(self.__dict__)

    def is_content_valid(self) -> bool:
        return toolbox.is_json_valid(self.content)