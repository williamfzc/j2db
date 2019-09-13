from pydantic import BaseModel


class JsonRequest(BaseModel):
    # for matching models
    table: str = ""
    # action
    action: str = ""
    # json
    content: str = ""
