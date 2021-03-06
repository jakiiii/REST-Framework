import os
import json
import requests

AUTH_ENDPOINT = "http://127.0.0.1:8000/api/auth/"
REFRESH_ENDPOINT = AUTH_ENDPOINT + "refresh/"

image_path = os.path.join(os.getcwd(), 'drf.png')


headers = {
    "Content-Type": "application/json",
}

data = {
    "username": 'jaki',
    "password": 'SADHIN101119',
}

r = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)
token = r.json()['token']
# print(token)

BASE_ENDPOINT = 'http://127.0.0.1:8000/api/status/'
ENDPOINT = BASE_ENDPOINT + '22/'

headers2 = {
    # "Content-Type": "application/json",
    "Authorization": "JWT " + token
}

data2 = {
    "content": "creating random content for permission test"
}

with open(image_path, 'rb') as image:
    file_data = {
        'image': image
    }
    r = requests.get(ENDPOINT, headers=headers2)
    # r = requests.put(ENDPOINT, data=data2, headers=headers2, files=file_data)
    # r = requests.post(BASE_ENDPOINT, data=data2, headers=headers2, files=file_data)
    print(r.text)


# AUTH_ENDPOINT = 'http://127.0.0.1:8000/api/auth/register/'
# REFRESH_ENDPOINT = AUTH_ENDPOINT + 'refresh/'
# ENDPOINT = 'http://127.0.0.1:8000/api/status/'
#
# image_path = os.path.join(os.getcwd(), 'drf.png')
#
#
# headers = {
#     "Content-Type": "application/json",
#     # "Authorization": "JWT " + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyMSwidXNlcm5hbWUiOiJ1c2VyMSIsImV4cCI6MTU0MzMwNzA0NSwiZW1haWwiOiJ1c2VyMUBqcXVyaXR5LmNvbSJ9.c_5e8sCojcqzgw0kPc_FNd74-GnrF3bNWHLe9Lz_oQ0"
# }
#
# data = {
#     "username": 'user2',
#     "email": 'user2@jqurity.com',
#     "password": 'password123',
#     "password2": 'password123',
# }
#
# r = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)
# token = r.json()  # ['token']
# print(token)

# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "JWT " + token
# }
#
#
# data = {
#     "content": "UPDATED DESCRIPTION"
# }

# posted_response = requests.put(ENDPOINT + str(23) + "/", data=json.dumps(data), headers=headers)
# print(posted_response.text)

# headers = {
#     # "Content-Type": "application/json",
#     "Authorization": "JWT " + token
# }
#
# with open(image_path, 'rb') as image:
#     file_data = {
#         'image': image
#     }
#     data = {
#         "content": "UPDATED DESCRIPTION"
#     }
#     posted_response = requests.put(ENDPOINT + str(23) + "/", data=data, headers=headers, files=file_data)
#     print(posted_response.text)


# get_endpoint = ENDPOINT + str(13)
# post_data = json.dumps({'content': 'some random content for test'})

# new_data = {
#     'token': token
# }
#
# new_r = requests.post(REFRESH_ENDPOINT, data=json.dumps(new_data), headers=headers)
# new_token = r.json()
# print(new_token)

# r = requests.get(get_endpoint)
# print(r.text)
#
# r2 = requests.get(get_endpoint)
# print(r2.status_code)
#
# post_headers = {
#     'content-type': 'application/json'
# }
#
# post_response = requests.post(ENDPOINT, data=post_data, headers=post_headers)
# print(post_response.text)


def do_img(method='get', data={},  is_json=True, img_path=None):
    headers = {}
    if is_json:
        headers['content-type'] = 'application/json'
        data = json.dumps(data)
    if img_path is not None:
        with open(image_path, 'rb') as image:
            file_data = {
                'image': image
            }
            r = requests.request(method, ENDPOINT, data=data, headers=headers, files=file_data)
    else:
        r = requests.request(method, ENDPOINT, data=data, headers=headers)
    print(r.text)
    print(r.status_code)
    return r


# do_img(method='post', data={'user': 1, 'content': ''}, is_json=False, img_path=image_path)
# do_img(method='put',
#        data={'id': 13, 'user': 1, 'content': 'random image content'},
#        is_json=False, img_path=image_path)


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
# do(method='delete', data={'id': 5})
# do(method='put', data={'id': 6, 'content': 'some content for put method testing.', 'user': 1})
# do(method='post', data={'id': 6, 'content': 'some content for post method testing.', 'user': 1})
