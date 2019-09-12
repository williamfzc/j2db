from pydantic import BaseModel


class JsonRequest(BaseModel):
    # for matching models
    tag: str = ""
    # json
    content: str = ""
