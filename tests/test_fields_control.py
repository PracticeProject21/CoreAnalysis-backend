import pytest

from fixtures import *
from backend.core_api.fields_control import (
    go_next_level,
    get_current_properties,
    delete_nested_from_properties,
    EndOfTree,
    InvalidFormat, delete_mentioned_property
)

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
            },
            {
                "name": "nested_param_2",
                "title": "nested_2_first",
                "values": [
                    {
                        "name": "one_nested",
                        "title": "One"
                    },
                    {
                        "name": "two_nested",
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
            },
            {
                "name": "nested_param_3",
                "title": "nested3",
                "values": [
                    {
                        "name": "one_3",
                        "title": "One 3"
                    },
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
    with pytest.raises(EndOfTree):
        go_next_level([{"name": "foo", "title": "FOO", "values":
                             [{"name": "ans_one", "title": "Answer"}]}], {"bar": "ans_one"})

    with pytest.raises(InvalidFormat):
        go_next_level([{"name": "foo", "title": "FOO", "values":
                             [{"name": "ans_one", "title": "Answer"}]}], {"foo": "ans_two"})

    with pytest.raises(InvalidFormat):
        go_next_level([{"name": "foo", "title": "FOO"}], {"foo": "ans_two"})

    with pytest.raises(InvalidFormat):
        go_next_level([{"names": "foo", "title": "FOO", "values":
                             [{"name": "ans_one", "title": "Answer"}]}], {"foo": "ans_one"})

    with pytest.raises(InvalidFormat):
        go_next_level([{"name": "foo", "title": "FOO", "values":
                             [{"names": "ans_one", "title": "Answer"}]}], {"foo": "ans_one"})


@pytest.mark.parametrize("forest,answer", [
        ([query], [
            {
                "name": "first_param",
                "title": "first",
                "values": [
                    {
                        "name": "first_ans",
                        "title": "FIRST A",
                    },
                    {
                        "name": "second_ans",
                        "title": "SECOND A",
                    }
                ]
            }
         ]
         ),
    (answers[1]['nested'][0]['values'][1]['nested'], answers[1]['nested'][0]['values'][1]['nested']),
    ([], [])
])
def test_delete_nested_from_properties(forest, answer):
    assert delete_nested_from_properties(forest) == answer


@pytest.mark.parametrize("properties,mentioned,answer", [
    (answers[0]['nested'], {"nested_param": "one"}, [answers[0]['nested'][1]]),
    (answers[0]['nested'], {"nested_param_wrong": "one"}, answers[0]['nested']),
    ([answers[0]['nested'][1]], {"nested_param_2": "one_nested"}, [])

])
def test_delete_mentioned_property(properties, mentioned, answer):
    delete_mentioned_property(properties, mentioned)
    assert properties == answer


@pytest.mark.parametrize("source,params,answer", (
        ([query], {"first_param": "first_ans"}, answers[0]['nested']),
        ([query], {"first_param": "second_ans"},
         [{
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
                 }
            ]
         },
             {
                 "name": "nested_param_3",
                 "title": "nested3",
                 "values": [
                     {
                         "name": "one_3",
                         "title": "One 3"
                     },
                 ]
             }
         ]),
        ([query], {"first_param": "second_ans", "nested_param_2": "two_2"}, [
            {
                 "name": "nested_param_3",
                 "title": "nested3",
                 "values": [
                     {
                         "name": "one_3",
                         "title": "One 3"
                     },
                 ]
             },
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
        ]),
        ([query], {"first_param": "first_ans", "nested_param": "one"}, [
            {
                "name": "nested_param_2",
                "title": "nested_2_first",
                "values": [
                    {
                        "name": "one_nested",
                        "title": "One"
                    },
                    {
                        "name": "two_nested",
                        "title": "Two"
                    }
                ]
            }
        ]),
        ([{"name": "one", "values": [{"name": "two"}]}], {"one": "two"}, [])
         ))
def test_get_properties(source: List[Dict], params: Dict, answer: List):
    assert get_current_properties(source, params) == answer
