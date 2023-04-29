"""Base types."""
from abc import ABC, abstractmethod
from typing import Any, Union

Context = dict[str, Any]
"""Template/expression context"""


class Evaluable(ABC):
    """Evaluable object."""

    @abstractmethod
    def evaluate(self, **context: Any) -> Any:
        """Evaluate this evaluable."""
        ...


LiteralValueTypes = (int, float, bool, str)
LiteralValue = Union[int, float, bool, str]
"""Literal value types."""

LiteralValueOrEvaluable = Union[LiteralValue, Evaluable]
"""A literal value, or an :class:`Evaluable`."""
