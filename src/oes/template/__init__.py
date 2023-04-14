"""OES Template Library"""

from oes.template.env import default_jinja2_env, get_jinja2_env, jinja2_env_context
from oes.template.expression import Expression
from oes.template.logic import Condition, LogicAnd, LogicOr, evaluate
from oes.template.serialization import configure_converter
from oes.template.template import Template
from oes.template.types import Context, Evaluable, Value, ValueOrEvaluable

__all__ = [
    "Value",
    "Evaluable",
    "ValueOrEvaluable",
    "Context",
    "default_jinja2_env",
    "jinja2_env_context",
    "get_jinja2_env",
    "Template",
    "Expression",
    "LogicAnd",
    "LogicOr",
    "Condition",
    "evaluate",
    "configure_converter",
]
