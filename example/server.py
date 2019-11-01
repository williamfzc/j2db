from j2db.server import Server
from j2db.db import MySQLManager, BaseModel
from j2db.auth import AuthManager, AuthUser

from sqlalchemy import Column, Integer, String

# configure your auth for safety
test_user = AuthUser(
    name="username",
    secret="pwd",
    allow_table=["some_table"],
)
AuthManager.add(test_user)


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
