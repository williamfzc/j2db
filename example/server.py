from j2db import auth
from j2db.server import Server
from j2db.db import MySQLManager, BaseModel

from sqlalchemy import Column, Integer, String

# configure your auth for safety
auth.AUTH_DICT = {
    "user_name": "YOUR_SECRET",
}


# register a model (table)
class SomeModel(BaseModel):
    __tablename__ = "some_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True)


# bind to db
# for test, you can use SQLite instead
manager = MySQLManager(
    url="127.0.0.1", port=33066, user="root", password="root", db_name="some_db"
)
manager.connect()
manager.add_model(SomeModel)

s = Server()
s.init_db(manager, create_tables=True)
s.start()
