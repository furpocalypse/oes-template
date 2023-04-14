"""Base types."""
from abc import ABC, abstractmethod
from typing import Any, Union

from cattrs import Converter

Context = dict[str, Any]
"""Template/expression context"""


class Evaluable(ABC):
    """Evaluable object."""

    @abstractmethod
    def evaluate(self, **context: Any) -> Any:
        """Evaluate this evaluable."""
        ...


ValueTypes = (int, float, bool, str)
Value = Union[int, float, bool, str]
ValueOrEvaluable = Union[Value, Evaluable]


def structure_value(v: object) -> object:
    if isinstance(v, ValueTypes):
        return v
    else:
        raise TypeError(f"Invalid value: {v!r}")


def structure_value_or_evaluable(converter: Converter, v) -> ValueOrEvaluable:
    if isinstance(v, str):
        # assume strings are template expressions
        return converter.structure(v, Evaluable)
    else:
        return converter.structure(v, Value)
