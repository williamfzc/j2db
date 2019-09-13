import requests
import pytest
import time
import json
from multiprocessing import Process
from sqlalchemy import Column, String, Integer
from loguru import logger

from json2db.server import Server
from json2db.server import BaseModel
from json2db.db import MySQLManager

URL_PREFIX = r"http://127.0.0.1:9410"
URL_HELLO = f"{URL_PREFIX}/"
URL_RAW = f"{URL_PREFIX}/api/json/raw"
URL_FORM = f"{URL_PREFIX}/api/json/form"


class SomeModel(BaseModel):
    __tablename__ = "some_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True)


REQUEST = {
    "both_invalid": {
        "table": "thisisinvalidtag",
        "action": "insert",
        "content": "{}abcde",
    },
    "invalid_table": {
        "table": "thisisinvalidtag",
        "action": "insert",
        "content": json.dumps({"id": 100, "name": "name1"}),
    },
    "invalid_content": {
        "table": "some_table",
        "action": "insert",
        "content": "{}cbdsalkj",
    },
    "both_valid": {
        "table": "some_table",
        "action": "insert",
        "content": json.dumps({"id": 101, "name": "name2"}),
    },
}


@pytest.fixture(scope="module", autouse=True)
def my_fixture():
    mysql_manager = MySQLManager(
        url="127.0.0.1", port=33066, user="root", password="root", db_name="some_test"
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
    request_data = REQUEST["invalid_content"]
    logger.info(request_data)
    resp = requests.post(URL_FORM, data=request_data)
    assert resp.ok
    assert resp.json()["error"] == "json_invalid"


def test_form_json_table_invalid():
    request_data = REQUEST["invalid_table"]
    logger.info(request_data)
    resp = requests.post(URL_FORM, data=request_data)
    assert resp.ok
    assert resp.json()["error"] == "table_invalid"


def test_form_json_valid():
    request_data = REQUEST["both_valid"]
    logger.info(request_data)
    resp = requests.post(URL_FORM, data=request_data)
    assert resp.ok
    assert resp.json() == {"status": "ok"}


def test_params_json_invalid():
    request_json = REQUEST["invalid_content"]
    logger.info(request_json)
    resp = requests.post(URL_RAW, json=request_json)
    assert resp.ok
    assert resp.json()["error"] == "json_invalid"
