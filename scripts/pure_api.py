import requests
import json
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
    r = requests.post(BASE_URL + ENDPOINT, data=json.dumps(new_data))
    print(r.headers)
    if r.status_code == requests.codes.ok:
        # print(r.json())
        return r.json()
    return r.text


def object_update():
    new_data = {
        'title': 'new random title',
        'content': 'new random  content'
    }
    r = requests.put(BASE_URL + ENDPOINT + "1", data=json.dumps(new_data))

    # new_data = {
    #     'id': 1,
    #     'title': 'get new title',
    #     'content': 'get random content'
    # }
    # r = requests.put(BASE_URL + ENDPOINT + "1", data=new_data)

    print(r.status_code)
    if r.status_code == requests.codes.ok:
        return r.json()
    return r.text


def object_delete():
    new_data = {
        'title': 'new random title',
        'content': 'new random content'
    }
    r = requests.delete(BASE_URL + ENDPOINT + "6")

    # new_data = {
    #     'id': 1,
    #     'title': 'get new title',
    #     'content': 'get random content'
    # }
    # r = requests.put(BASE_URL + ENDPOINT + "1", data=new_data)

    print(r.status_code)
    if r.status_code == requests.codes.ok:
        return r.json()
    return r.text


# get_list()
print(create_update())
# print(object_update())
# print(object_delete())
