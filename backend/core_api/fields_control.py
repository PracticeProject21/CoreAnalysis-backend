import yaml
from typing import List, Dict

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
            raise Exception('Invalid format')
        try:
            nested = next(x for x in found if x['name'] == _params[name])['nested']
        except StopIteration as e:
            Exception('Invalid format')
        except KeyError as k:
            if k.args[0] == 'nested':
                return []
            else:
                raise Exception('Invalid format')
        else:
            return nested
    raise Exception('No matching params')

