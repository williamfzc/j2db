from pydantic import BaseModel


class JsonRequest(BaseModel):
    # for matching models
    tag: str = ""
    # action
    action: str = ""
    # json
    content: str = ""
