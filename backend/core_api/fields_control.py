import yaml
from typing import List, Dict


class InvalidFormat(Exception):
    def __init__(self, field, key):
        self.message = "Field {} has no {} key".format(field, key)


class EndOfTree(Exception):
    pass


with open('fields.yml', 'r') as file:
    config = yaml.safe_load(file)


def go_next_level(source: List[Dict], params: Dict) -> List[Dict]:
    _params = params.copy()
    for name in _params.keys():
        try:
            found = next(x for x in source if x['name'] == name)['values']
        except StopIteration as e:
            continue
        except KeyError as e:
            raise InvalidFormat(name, e.args[0])
        try:
            nested = next(x for x in found if x['name'] == _params[name])['nested']
        except StopIteration as e:
            raise InvalidFormat(_params[name], 'suitable')
        except KeyError as k:
            if k.args[0] == 'nested':
                return []
            else:
                raise InvalidFormat(_params[name], k.args[0])
        else:
            return nested
    raise EndOfTree()


def delete_nested_from_properties(forest: List[Dict]) -> List[Dict]:
    """
    delete all nested properties from values and return a new list
    """
    out = []
    try:
        for tree in forest:
            out_tree = tree.copy()
            out_tree['values'] = []
            for val in tree['values']:
                out_val = val.copy()
                if out_val.get('nested'):
                    del out_val['nested']
                out_tree['values'].append(out_val)
            out.append(out_tree)
        return out
    except KeyError as e:
        raise InvalidFormat('', e.args[0])


def delete_mentioned_property(properties: List[Dict], mention: Dict) -> None:
    """Delete properties, whose names mentioned in dict.
    Replace properties in-place"""
    for name in mention.keys():
        try:
            found_id = next(idx for idx, x in enumerate(properties) if x['name'] == name)
        except StopIteration as e:
            continue
        properties.pop(found_id)


def get_current_properties(config: List[Dict], params: Dict) -> List[Dict]:
    current_level = config
    properties = []
    while True:
        new_properties = delete_nested_from_properties(current_level)
        delete_mentioned_property(new_properties, params)
        properties.extend(new_properties)
        try:
            current_level = go_next_level(current_level, params)
        except EndOfTree:
            return properties
