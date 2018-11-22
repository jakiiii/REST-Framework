import json
import requests

ENDPOINT = 'http://127.0.0.1:8000/api/status/'


def do(method='get', data={},  is_json=True):
    headers = {}
    if is_json:
        headers['content-type'] = 'application/json'
        data = json.dumps(data)
    r = requests.request(method, ENDPOINT, data=data, headers=headers)
    print(r.text)
    print(r.status_code)
    return r


# do(data={'id': 6})
do(method='delete', data={'id': 5})
# do(method='put', data={'id': 6, 'content': 'some content for put method testing.', 'user': 1})
# do(method='post', data={'id': 6, 'content': 'some content for post method testing.', 'user': 1})
