"""Logic objects."""
from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING, Any, Union

from attrs import frozen

from oes.template import Expression
from oes.template.types import (
    Context,
    Evaluable,
    LiteralValueOrEvaluable,
    LiteralValueTypes,
)

if TYPE_CHECKING:
    from cattrs import Converter


@frozen
class LogicAnd(Evaluable):
    """Logic AND."""

    and_: Condition

    def evaluate(self, **context: Any) -> bool:
        return all(_eval_condition(self.and_, context))


@frozen
class LogicOr(Evaluable):
    """Logic OR."""

    or_: Condition

    def evaluate(self, **context: Any) -> bool:
        return any(_eval_condition(self.or_, context))


LogicExpression = Union[
    LiteralValueOrEvaluable,
    LogicAnd,
    LogicOr,
    None,
]
"""A logic expression.

One of:
  - A literal value (str, int, float, bool)
  - An :class:`Evaluable` (i.e. a template expression)
  - A :class:`LogicAnd`
  - A :class:`LogicOr`
  - ``None``
"""

Condition = Union[Sequence, LogicExpression]
"""A single :class:`LogicExpression` or a sequence of them.

Sequences are evaluated as an implicit logic AND of the items.
"""


def _as_iterable(expr: Condition) -> Iterable[Condition]:
    """Turn scalars into an iterable of only that scalar."""
    if isinstance(expr, Sequence) and not isinstance(expr, str):
        yield from expr
    else:
        yield expr


def _eval(obj: object, context: Context) -> Any:
    """Return a literal value, or evaluate an evaluable."""
    if isinstance(obj, Evaluable):
        return obj.evaluate(**context)
    else:
        return obj


def _eval_condition(expr: Condition, context: Context) -> Iterable[Any]:
    """Evaulate a scalar or sequence, yielding the results of each."""
    for e in _as_iterable(expr):
        yield _eval(e, context)


def evaluate(cond: Condition, context: Context) -> bool:
    """Evaluate a :class:`Condition`."""
    return all(_eval_condition(cond, context))


def structure_logic_expression(converter: Converter, v: object):  # noqa: CCR001
    if isinstance(v, str):
        # All strings are treated as template expressions
        return converter.structure(v, Expression)
    elif v is None or isinstance(v, LiteralValueTypes):
        return v
    elif isinstance(v, dict) and "and" in v:
        return structure_and(converter, v)
    elif isinstance(v, dict) and "or" in v:
        return structure_or(converter, v)
    else:
        raise TypeError(f"Invalid type: {v!r}")


def structure_and(converter: Converter, v: object) -> LogicAnd:
    if isinstance(v, dict) and "and" in v:
        exprs = v["and"]
    else:
        exprs = v

    return LogicAnd(structure_condition(converter, exprs))


def structure_or(converter: Converter, v: object) -> LogicOr:
    if isinstance(v, dict) and "or" in v:
        exprs = v["or"]
    else:
        exprs = v

    return LogicOr(structure_condition(converter, exprs))


def structure_condition(converter: Converter, v: object):
    if isinstance(v, Sequence) and not isinstance(v, str):
        return tuple(structure_logic_expression(converter, c) for c in v)
    else:
        return structure_logic_expression(converter, v)


def unstructure_and(converter: Converter, v: LogicAnd) -> dict:
    return {"and": converter.unstructure(v.and_)}


def unstructure_or(converter: Converter, v: LogicOr) -> dict:
    return {"or": converter.unstructure(v.or_)}
