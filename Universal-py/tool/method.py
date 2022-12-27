import json
from functools import wraps

import tool.element as element


def nan_to_null(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).replace('nan', 'null')

    return wrapper


def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def convert_template(template: dict) -> dict:
    # convert the template detail to the class
    converted_template = {}
    for key, value in template.items():
        if isinstance(value, str):
            converted_template[key] = value
        elif isinstance(value, list):
            converted_template[key] = [convert_template(i) for i in value]
        elif isinstance(value, dict):
            converted_template[key] = convert_template(value)
        elif isinstance(value, element.Node):
            converted_template[key] = value.attributes()
    return converted_template
