import requests
import pytest
import time
from multiprocessing import Process
from sqlalchemy import Column, String, Integer

from json2db.server import Server
from json2db.server import BaseModel
from json2db.db import MySQLManager

URL_PREFIX = r"http://127.0.0.1:9410"


class SomeModel(BaseModel):
    __tablename__ = "some_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True)


@pytest.fixture(scope="module", autouse=True)
def my_fixture():
    manager = MySQLManager(
        url="127.0.0.1",
        port=3306,
        user="user",
        password="pwd",
        db_name="some_test",
    )
    manager.connect()

    s = Server()
    s.init_db(manager)
    p = Process(target=s.start)
    p.start()
    time.sleep(3)
    yield
    p.kill()


def test_hello():
    resp = requests.get(f"{URL_PREFIX}/")
    assert resp.ok


def test_form_json_invalid():
    resp = requests.post(
        f"{URL_PREFIX}/api/json/form", data={"tag": "abc", "content": "is{}#@!$"}
    )
    assert resp.ok
    assert resp.json()["error"] == "json_invalid"


def test_params_json_invalid():
    resp = requests.post(
        f"{URL_PREFIX}/api/json/params", json={"tag": "abc", "content": "is{}#@!$"}
    )
    assert resp.ok
    assert resp.json()["error"] == "json_invalid"
