import pytest
from cattrs.preconf.json import make_converter

from oes.template import (
    Expression,
    LogicAnd,
    LogicOr,
    structure_condition,
    structure_expression,
    unstructure_and,
    unstructure_expression,
    unstructure_or,
)
from oes.template.logic import Condition, evaluate

converter = make_converter()
converter.register_structure_hook(Expression, lambda v, t: structure_expression(v))
converter.register_structure_hook(
    Condition, lambda v, t: structure_condition(converter, v)
)
converter.register_unstructure_hook(
    Expression,
    lambda v: unstructure_expression(v),
)
converter.register_unstructure_hook(LogicAnd, lambda v: unstructure_and(converter, v))
converter.register_unstructure_hook(LogicOr, lambda v: unstructure_or(converter, v))

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
        ("true", {"or": (True, False)}),
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
