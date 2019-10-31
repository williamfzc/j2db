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

URL_PREFIX = r"http://127.0.0.1:9410"
URL_HELLO = f"{URL_PREFIX}/"
URL_RAW = f"{URL_PREFIX}/api/json/raw"
URL_FORM = f"{URL_PREFIX}/api/json/form"

DB_USER = "root"
DB_PWD = "root"
DB_URL = "127.0.0.1"
DB_PORT = 33066
DB_NAME = "some_db"
TABLE_NAME = "some_table"

counter = itertools.count()


class SomeModel(BaseModel):
    __tablename__ = "some_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True)


def get_data(data_type: str):
    if data_type == "both_invalid":
        return {
            "table": "thisisinvalidtag",
            "action": "thisisinvalidaction",
            "content": "{}abcde",
            "secret": "williamfzc",
        }

    new_id = next(counter)
    new_name = f"name_{new_id}"

    if data_type == "invalid_table":
        return {
            "table": "thisisinvalidtag",
            "action": "insert",
            "content": json.dumps({"id": new_id, "name": new_name}),
            "secret": "williamfzc",
        }
    elif data_type == "invalid_action":
        return {
            "table": TABLE_NAME,
            "action": "invalidaction",
            "content": json.dumps({"id": new_id, "name": new_name}),
            "secret": "williamfzc",
        }
    elif data_type == "invalid_content":
        return {
            "table": TABLE_NAME,
            "action": "insert",
            "content": "{}123344adsf",
            "secret": "williamfzc",
        }
    elif data_type == "both_valid":
        return {
            "table": TABLE_NAME,
            "action": "insert",
            "content": json.dumps({"id": new_id, "name": new_name}),
            "secret": "williamfzc",
        }


@pytest.fixture(scope="module", autouse=True)
def my_fixture():
    mysql_manager = MySQLManager(
        url=DB_URL, port=DB_PORT, user=DB_USER, password=DB_PWD, db_name=DB_NAME
    )
    manager = mysql_manager
    manager.connect()
    manager.add_model(SomeModel)

    s = Server()
    s.init_db(manager, create_tables=True)
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
    assert resp.json()["error"] == "table_invalid"


def test_form_json_valid():
    request_data = get_data("both_valid")
    logger.info(request_data)
    resp = requests.post(URL_FORM, data=request_data)
    assert resp.ok
    assert resp.json() == {"status": "ok"}


def test_params_json_invalid():
    request_json = get_data("invalid_content")
    logger.info(request_json)
    resp = requests.post(URL_RAW, json=request_json)
    assert resp.ok
    assert resp.json()["error"] == "json_invalid"


def test_pressure():
    request_list = (get_data("both_valid") for _ in range(5000))
    for each in request_list:
        resp = requests.post(URL_RAW, json=each)
        assert resp.ok
        assert resp.json()["status"] == "ok"
