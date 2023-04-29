"""OES Template Library"""

from oes.template.env import default_jinja2_env, get_jinja2_env, jinja2_env_context
from oes.template.expression import (
    Expression,
    structure_expression,
    unstructure_expression,
)
from oes.template.logic import (
    Condition,
    LogicAnd,
    LogicOr,
    evaluate,
    structure_condition,
    unstructure_and,
    unstructure_or,
)
from oes.template.template import Template, structure_template, unstructure_template
from oes.template.types import Context, Evaluable, LiteralValue, LiteralValueOrEvaluable

__all__ = [
    "LiteralValue",
    "Evaluable",
    "LiteralValueOrEvaluable",
    "Context",
    "default_jinja2_env",
    "jinja2_env_context",
    "get_jinja2_env",
    "Template",
    "structure_template",
    "unstructure_template",
    "Expression",
    "structure_expression",
    "unstructure_expression",
    "LogicAnd",
    "LogicOr",
    "Condition",
    "evaluate",
    "structure_condition",
    "unstructure_and",
    "unstructure_or",
]
