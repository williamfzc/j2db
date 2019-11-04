import requests
import pytest
import time
import json
import itertools
from multiprocessing import Process
from sqlalchemy import Column, String, Integer
from loguru import logger

from j2db.server import Server
from j2db.server import BaseModel
from j2db.db import MySQLManager
from j2db.auth import AuthManager, AuthUser
from j2db.handler import EventHandler
from j2db.models import EventModel
from j2db.client import J2DBClient

J2DB_SERVER_ADDRESS = "127.0.0.1"
J2DB_SERVER_PORT = 9410
URL_PREFIX = f"http://{J2DB_SERVER_ADDRESS}:{J2DB_SERVER_PORT}"
URL_HELLO = f"{URL_PREFIX}/"
URL_RAW = f"{URL_PREFIX}/api/json/raw"
URL_FORM = f"{URL_PREFIX}/api/json/form"

DB_USER = "root"
DB_PWD = "root"
DB_IP_ADDRESS = "127.0.0.1"
DB_PORT = 33066
DB_NAME = "some_db"
TABLE_NAME = "some_table"
AUTH_USER_NAME = "williamfzc"
AUTH_PWD = "pwd"
AUTH_STR = f"{AUTH_USER_NAME}:{AUTH_PWD}"
test_user = AuthUser(
    name=AUTH_USER_NAME,
    secret=AUTH_PWD,
    allow_table=[TABLE_NAME],
)
secret_str = f"{test_user.name}:{test_user.secret}"
AuthManager.add(test_user)

counter = itertools.count()


class SomeModel(BaseModel):
    __tablename__ = "some_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True)


class NewHandler(EventHandler):
    def before_auth(self, event: EventModel) -> EventModel:
        print("hey i am edited")
        return event


def get_data(data_type: str):
    if data_type == "both_invalid":
        return {
            "table": "thisisinvalidtag",
            "action": "thisisinvalidaction",
            "content": "{}abcde",
            "secret": secret_str,
        }

    new_id = next(counter)
    new_name = f"name_{new_id}"

    if data_type == "invalid_table":
        return {
            "table": "thisisinvalidtag",
            "action": "insert",
            "content": json.dumps({"id": new_id, "name": new_name}),
            "secret": secret_str,
        }
    elif data_type == "invalid_action":
        return {
            "table": TABLE_NAME,
            "action": "invalidaction",
            "content": json.dumps({"id": new_id, "name": new_name}),
            "secret": secret_str,
        }
    elif data_type == "invalid_content":
        return {
            "table": TABLE_NAME,
            "action": "insert",
            "content": "{}123344adsf",
            "secret": secret_str,
        }
    elif data_type == "both_valid":
        return {
            "table": TABLE_NAME,
            "action": "insert",
            "content": json.dumps({"id": new_id, "name": new_name}),
            "secret": secret_str,
        }


@pytest.fixture(scope="module", autouse=True)
def my_fixture():
    mysql_manager = MySQLManager(
        url=DB_IP_ADDRESS, port=DB_PORT, user=DB_USER, password=DB_PWD, db_name=DB_NAME
    )
    manager = mysql_manager
    manager.connect()
    manager.add_model(SomeModel)
    new_handler = NewHandler(manager)

    s = Server()
    s.init_db(manager, create_tables=True)
    s.init_handler(new_handler)
    p = Process(target=s.start)
    p.start()
    time.sleep(3)
    yield
    p.kill()


def test_hello():
    resp = requests.get(URL_HELLO)
    assert resp.ok
    assert resp.json()["Hello"] == "World"


def test_form_json_content_invalid():
    request_data = get_data("invalid_content")
    logger.info(request_data)
    resp = requests.post(URL_FORM, data=request_data)
    assert resp.ok
    assert resp.json()["error"] == "json_invalid"


def test_form_json_table_invalid():
    request_data = get_data("invalid_table")
    logger.info(request_data)
    resp = requests.post(URL_FORM, data=request_data)
    assert resp.ok
    # validate flow: auth -> table -> content
    # so, invalid table -> invalid auth
    assert resp.json()["error"] == "auth_invalid"


def test_form_json_valid():
    request_data = get_data("both_valid")
    logger.info(request_data)
    resp = requests.post(URL_FORM, data=request_data)
    assert resp.ok
    assert resp.json()["error"] == ""


def test_form_json_valid_with_client():
    cli = J2DBClient(
        J2DB_SERVER_ADDRESS,
        J2DB_SERVER_PORT,
        TABLE_NAME,
        AUTH_STR,
    )
    data = get_data("both_valid")["content"]
    resp = cli.send(data)
    assert resp.ok
    assert resp.json()["error"] == ""


def test_params_json_invalid():
    request_json = get_data("invalid_content")
    logger.info(request_json)
    resp = requests.post(URL_RAW, json=request_json)
    assert resp.ok
    assert resp.json()["error"] == "json_invalid"


def test_pressure():
    # TODO threading or async
    request_list = (get_data("both_valid") for _ in range(5000))
    for each in request_list:
        resp = requests.post(URL_RAW, json=each)
        assert resp.ok
        assert resp.json()["error"] == ""
