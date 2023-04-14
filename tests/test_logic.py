import pytest
from cattrs.preconf.json import make_converter

from oes.template.logic import Condition, evaluate
from oes.template.serialization import configure_converter

converter = make_converter()

configure_converter(converter)

cases = [
    (
        True,
        {},
        True,
    ),
    (
        False,
        {},
        False,
    ),
    (
        "0",
        {},
        False,
    ),
    (
        "false",
        {},
        False,
    ),
    (
        "value",
        {"value": False},
        False,
    ),
    (
        "value",
        {"value": True},
        True,
    ),
    (
        {
            "or": (
                "1 + 1 == 2",
                "0",
            )
        },
        {},
        True,
    ),
    (
        {
            "and": (
                "1 + 1 == 2",
                "0",
            )
        },
        {},
        False,
    ),
    (
        {"and": ("a + b == 10", {"or": "c"})},
        {"a": 5, "b": 5, "c": 0},
        False,
    ),
    (
        {"and": ("a + b == 10", {"or": "c"})},
        {"a": 5, "b": 4, "c": 1},
        False,
    ),
    (
        {"and": ("a + b == 10", {"or": "c"})},
        {"a": 5, "b": 5, "c": 1},
        True,
    ),
    (
        ("true", "false"),
        {},
        False,
    ),
    (
        ("true", "1"),
        {},
        True,
    ),
    (
        ("true", (True, False)),
        {},
        True,
    ),
]


@pytest.mark.parametrize(
    "src, context, value",
    cases,
)
def test_logic_parsing_and_eval(src, context, value):
    condition = converter.structure(src, Condition)
    result = evaluate(condition, context)
    assert result == value


@pytest.mark.parametrize(
    "case",
    [
        "a",
        {"and": ["a", 2]},
        ["a", {"or": [{"and": "1 + 1 == 2"}, 0]}],
    ],
)
def test_logic_parsing_unstructure(case):
    condition = converter.structure(case, Condition)
    back = converter.unstructure(condition, Condition)
    assert back == case
