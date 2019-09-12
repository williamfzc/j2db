from json2db.server import Server
from json2db.db import SQLiteManager, BaseModel

from sqlalchemy import Column, Integer, String


class SomeModel(BaseModel):
    __tablename__ = "some_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True)


manager = SQLiteManager(path_to_db="/path/to/your.db")
manager.connect()
manager.add_model(SomeModel)

s = Server()
s.init_db(manager, create_tables=True)
s.start()
