from datetime import datetime
import json


def fill_dates(item):
    for key in ['created_at', 'updated_at', 'closed_at']:
        if item[key]:
            item[key] = datetime.strptime(item[key], '%Y-%m-%dT%H:%M:%SZ')
    return item


def load_data(filename):
    with open(filename) as f:
        data = json.load(f)
    return [fill_dates(item) for item in data]
