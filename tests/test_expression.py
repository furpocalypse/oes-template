import pytest
from jinja2 import Undefined

from oes.template.expression import Expression


@pytest.mark.parametrize(
    "src, context, value",
    [
        ("100", {}, 100),
        ("'str'", {}, "str"),
        ("1 + a + b", {"a": 2, "b": 3}, 6),
    ],
)
def test_expression(src, context, value):
    expr = Expression(src)
    res = expr.evaluate(**context)
    assert res == value


def test_undefined():
    expr = Expression("missing")
    res = expr.evaluate()
    assert isinstance(res, Undefined)
