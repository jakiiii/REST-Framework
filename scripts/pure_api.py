import requests

BASE_URL = 'http://127.0.0.1:8000/'
ENDPOINT = 'api/updates/'


def get_list():
    r = requests.get(BASE_URL + ENDPOINT)
    data = r.json()
    for obj in data:
        if obj['id'] == 1:
            r2 = requests.get(BASE_URL + ENDPOINT + str(obj['id']))
            print(r2.json())
    return data


def create_update():
    new_data = {
        'user': 1,
        'title': 'some random title',
        'content': 'some random content'
    }
    r = requests.post(BASE_URL + ENDPOINT + "1", data=new_data)
    print(r.headers)
    if r.status_code == requests.codes.ok:
        # print(r.json())
        return r.json()
    return r.text


# get_list()
print(create_update())
