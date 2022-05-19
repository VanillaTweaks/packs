import json


def json_str(value: object):
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
    )
