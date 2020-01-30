import json
import os
import sys

def get_server_info_value(key: str):
    with open(os.path.join(sys.path[0], 'mysite/server_info.json'), mode='rt', encoding='utf-8') as file:
        data = json.load(file)
        for k, v in data.items():
            if k == key:
                return v
        raise ValueError('can\'t find information.')

