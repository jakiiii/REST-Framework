import json


def is_json(json_data):
    try:
        true_json = json.loads(json_data)
        is_valied = True
    except ValueError:
        is_valied = False
    return is_valied
