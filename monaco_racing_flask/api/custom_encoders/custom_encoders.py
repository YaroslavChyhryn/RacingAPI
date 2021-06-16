import dataclasses
import datetime
import json
from flask import make_response
import simplexml


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return str(obj)
        elif isinstance(obj, datetime.timedelta):
            return str(obj)
        elif dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        return json.JSONEncoder.default(self, obj)


def output_json(data, code, headers=None):
    dumped = json.dumps(data, cls=CustomJsonEncoder)
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


def output_xml(data, code, headers=None):
    """Makes a Flask response with a XML encoded body"""
    if dataclasses.is_dataclass(data):
        data = dataclasses.asdict(data)
    resp = make_response(simplexml.dumps({'response': data}), code)
    resp.headers.extend(headers or {})
    return resp
