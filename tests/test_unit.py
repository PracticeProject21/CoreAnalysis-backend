from fixtures import *
from backend.core_api.fields_control import go_next_level

from typing import List, Dict

first_param = {
        "name": "first_param",
        "title": "first",
        "values": []
}

answers = [
    {
        "name": "first_ans",
        "title": "FIRST A",
        "nested": [
            {
                "name": "nested_param",
                "title": "nested",
                "values": [
                    {
                        "name": "one",
                        "title": "One"
                    },
                    {
                        "name": "two",
                        "title": "Two"
                    }
                ]
            }
        ]
    },
    {
        "name": "second_ans",
        "title": "SECOND A",
        "nested": [
            {
                "name": "nested_param_2",
                "title": "nested",
                "values": [
                    {
                        "name": "one_2",
                        "title": "One 2"
                    },
                    {
                        "name": "two_2",
                        "title": "Two 2",
                        "nested":
                        [
                            {
                                "name": "nes_nes_param",
                                "title": "Deep param",
                                "values":
                                [
                                    {
                                        "name": "deep_val",
                                        "title": "Deep val",
                                    },
                                    {
                                        "name": "very_deep_val",
                                        "title": "VERY Deep val",
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
]

query = first_param.copy()
query['values'].extend(answers)


@pytest.mark.parametrize("source,params,answer", [
    ([query], {"first_param": "first_ans"}, answers[0]['nested']),
    ([query], {'nested_param_2': 'very_deep_val', 'first_param': 'second_ans'}, answers[1]['nested']),
    (answers[1]['nested'], {'first_param': 'second_ans', 'nested_param_2': 'two_2', 'nes_nes_param': 'deep_val'},
     answers[1]['nested'][0]['values'][1]['nested']),
    (answers[1]['nested'], {'first_param': 'second_ans', 'nested_param_2': 'one_2'}, [])
])
def test_go_next_level(source: List[Dict], params: Dict, answer: List):
    assert go_next_level(source, params) == answer


def test_wrong_go_next_level():
    with pytest.raises(Exception):
        go_next_level([{"name": "foo", "title": "FOO", "values":
                             [{"name": "ans_one", "title": "Answer"}]}], {"bar": "ans_one"})
