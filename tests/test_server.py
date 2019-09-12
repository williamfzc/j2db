import requests
import pytest
import time
from multiprocessing import Process

from json2db.server import start_server

URL_PREFIX = r'http://127.0.0.1:9410'


@pytest.fixture(scope="module", autouse=True)
def my_fixture():
    p = Process(target=start_server, args=(9410,))
    p.start()
    time.sleep(3)
    yield
    p.kill()


def test_hello():
    resp = requests.get(f'{URL_PREFIX}/')
    assert resp.ok


def test_form_json_invalid():
    resp = requests.post(
        f'{URL_PREFIX}/api/json/form',
        data={
            'tag': 'abc',
            'content': 'is{}#@!$'
        }
    )
    assert resp.ok
    assert resp.json()['error'] == 'json_invalid'


def test_params_json_invalid():
    resp = requests.post(
        f'{URL_PREFIX}/api/json/params',
        json={
            'tag': 'abc',
            'content': 'is{}#@!$'
        }
    )
    assert resp.ok
    assert resp.json()['error'] == 'json_invalid'
