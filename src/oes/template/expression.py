"""Template expression module."""
from typing import Any

import jinja2.environment
from attrs import Factory, field, frozen

from oes.template.env import get_jinja2_env
from oes.template.types import Evaluable


def _compile(expr):
    env = get_jinja2_env()
    return env.compile_expression(expr.source, undefined_to_none=False)


@frozen(repr=False)
class Expression(Evaluable):
    """Template expression"""

    source: str
    """The template source."""

    _compiled: jinja2.environment.TemplateExpression = field(
        init=False,
        eq=False,
        default=Factory(_compile, takes_self=True),
    )

    def __getstate__(self):
        return {"source": self.source}

    def __setstate__(self, state):
        object.__setattr__(self, "source", state["source"])
        object.__setattr__(self, "_compiled", _compile(self))

    def __repr__(self):
        return repr(self.source)

    def evaluate(self, **context: Any) -> Any:
        return self._compiled(**context)


def structure_expression(v: object) -> Expression:
    if isinstance(v, str):
        return Expression(v)
    else:
        raise TypeError(f"Invalid template expression: {v!r}")


def unstructure_expression(v: Expression) -> str:
    return v.source
