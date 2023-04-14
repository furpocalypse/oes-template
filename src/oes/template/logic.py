"""Logic objects."""
from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any, Union

from attrs import frozen
from cattrs import Converter

from oes.template.types import Context, Evaluable, Value, ValueTypes


@frozen
class LogicAnd(Evaluable):
    """Logic AND."""

    and_: LogicExpressions

    def evaluate(self, **context: Any) -> bool:
        return all(_eval_expr(self.and_, context))


@frozen
class LogicOr(Evaluable):
    """Logic OR."""

    or_: LogicExpressions

    def evaluate(self, **context: Any) -> bool:
        return any(_eval_expr(self.or_, context))


LogicExpression = Union[
    Value,
    Evaluable,
    LogicAnd,
    LogicOr,
    None,
]

LogicExpressions = Union[Sequence, LogicExpression]

Condition = LogicExpressions


def _iter_expr(expr: LogicExpressions) -> Iterable[LogicExpression]:
    if isinstance(expr, Sequence) and not isinstance(expr, str):
        yield from expr
    else:
        yield expr


def _eval(obj: object, context: Context) -> Any:
    if isinstance(obj, Evaluable):
        return obj.evaluate(**context)
    else:
        return obj


def _eval_expr(expr: LogicExpressions, context: Context) -> Iterable[Any]:
    for e in _iter_expr(expr):
        yield _eval(e, context)


def evaluate(cond: Condition, context: Context) -> bool:
    """Evaluate a :class:`Condition`."""
    return all(_eval_expr(cond, context))


def _structure_and_or(converter: Converter, v):
    if "and" in v:
        return converter.structure(
            {**v, "and_": v["and"]},
            LogicAnd,
        )
    elif "or" in v:
        return converter.structure(
            {
                **v,
                "or_": v["or"],
            },
            LogicOr,
        )
    else:
        raise ValueError(f"Invalid expression: {v!r}")


def structure_logic_expressions(converter: Converter, v: object) -> object:
    if isinstance(v, dict):
        return _structure_and_or(converter, v)
    elif isinstance(v, Sequence) and not isinstance(v, str):
        # implicit AND
        return tuple(converter.structure(e, LogicExpressions) for e in v)
    elif isinstance(v, str):
        # Assume strings are template expressions
        return converter.structure(v, Evaluable)
    elif v is None or isinstance(v, ValueTypes):
        return v

    raise ValueError(f"Invalid expression: {v!r}")


def unstructure_and(converter: Converter, v: LogicAnd) -> dict[str, Any]:
    return {"and": converter.unstructure(v.and_)}


def unstructure_or(converter: Converter, v: LogicOr) -> dict[str, Any]:
    return {"or": converter.unstructure(v.or_)}
