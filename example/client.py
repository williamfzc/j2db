# in client, all you need is sending a request with JSON
import requests
import json

request_data = {
    "table": "some_table",
    "action": "insert",
    "content": json.dumps({"id": 9647, "name": "hello9647"}),
    "secret": "username:pwd",
}
url = "http://127.0.0.1:9410/api/json/form"
resp = requests.post(url, data=request_data)
assert resp.ok
print(resp.text)
