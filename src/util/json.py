import json
import datetime
from dateutil import parser

class RegisteredTypes(object):
    Types = {}

def register_type(target_type):
    RegisteredTypes.Types[target_type.__name__] = target_type

def obj_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def to_collection_item_json(obj):
    return [{'Type': obj.__class__.__name__}, obj.__dict__]


def to_collection_items(json_data):
    decoded_items = []
    json_items = json.loads(json_data)
    for items in json_items:
        type_name = items[0]['Type']
        name_values = items[1]
        c = RegisteredTypes.Types[type_name]
        obj = c()
        for key in name_values.keys():
            if '_date' in key:
                if name_values[key]:
                    setattr(obj, key, parser.parse(name_values[key]))
            else:
                setattr(obj, key, name_values[key])
        decoded_items.append(obj)
    return decoded_items

def to_object(json_data):
    return json.loads(json_data)


def to_collection_json(col):
    json_frm = []
    for item in col:
        json_frm.append(to_collection_item_json(item))
    return json.dumps(json_frm, default=obj_converter)

def to_json(obj):
    return json.dumps(obj, default=obj_converter)
