import yaml
from typing import List, Dict


class InvalidFormat(Exception):
    def __init__(self, field, key):
        self.message = "Field {} has no {} key".format(field, key)


class EndOfTree(Exception):
    pass

# with open('fields.yml', 'r') as file:
#     config = yaml.safe_load(file)


def get_current_properties(**params):
    pass


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

