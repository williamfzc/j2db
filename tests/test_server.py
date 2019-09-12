import requests
import pytest
import time
import json
from multiprocessing import Process
from sqlalchemy import Column, String, Integer

from json2db.server import Server
from json2db.server import BaseModel
from json2db.db import MySQLManager, SQLiteManager

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
        "tag": "thisisinvalidtag",
        "action": "insert",
        "content": "{}abcde",
    },
    "invalid_tag": {
        "tag": "thisisinvalidtag",
        "action": "insert",
        "content": json.dumps({"id": 100, "name": "name1"}),
    },
    "invalid_content": {
        "tag": "some_table",
        "action": "insert",
        "content": "{}cbdsalkj",
    },
    "both_valid": {
        "tag": "some_table",
        "action": "insert",
        "content": json.dumps({"id": 101, "name": "name2"}),
    },
}

# managers
mysql_manager = MySQLManager(
    url="127.0.0.1", port=33066, user="root", password="root", db_name="some_test"
)


sqlite_manager = SQLiteManager("/Users/fengzhangchi/github_workspace/json2db/test.db")


@pytest.fixture(scope="module", autouse=True)
def my_fixture():
    manager = sqlite_manager
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
    resp = requests.post(URL_FORM, data=REQUEST["invalid_content"])
    assert resp.ok
    assert resp.json()["error"] == "json_invalid"


def test_form_json_tag_invalid():
    resp = requests.post(URL_FORM, data=REQUEST["invalid_tag"])
    assert resp.ok
    assert resp.json()["error"] == "tag_invalid"


def test_form_json_valid():
    resp = requests.post(URL_FORM, data=REQUEST["both_valid"])
    assert resp.ok
    assert resp.text == '"ok"'


def test_params_json_invalid():
    resp = requests.post(URL_RAW, json=REQUEST["invalid_content"])
    assert resp.ok
    assert resp.json()["error"] == "json_invalid"
