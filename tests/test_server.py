import requests
import pytest
import time
from multiprocessing import Process

from json2db.server import start_server


@pytest.fixture(scope="module", autouse=True)
def my_fixture():
    p = Process(target=start_server, args=(9410,))
    p.start()
    time.sleep(3)
    yield
    p.kill()


def test_hello():
    resp = requests.get('http://127.0.0.1:9410/')
    assert resp.ok
