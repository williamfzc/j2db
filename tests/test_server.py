from json2db import server


def test_hello():
    assert server.hello() == 'world'
