import json


def pretty_dump(data):
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
