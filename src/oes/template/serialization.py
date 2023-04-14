"""Serialization module."""
from cattrs import Converter

from oes.template.expression import (
    Expression,
    structure_expression,
    unstructure_expression,
)
from oes.template.logic import (
    LogicAnd,
    LogicExpressions,
    LogicOr,
    structure_logic_expressions,
    unstructure_and,
    unstructure_or,
)
from oes.template.template import Template, structure_template, unstructure_template
from oes.template.types import (
    Evaluable,
    Value,
    ValueOrEvaluable,
    structure_value,
    structure_value_or_evaluable,
)


def configure_converter(converter: Converter):
    converter.register_structure_hook(Value, lambda v, t: structure_value(v))
    converter.register_structure_hook(
        ValueOrEvaluable, lambda v, t: structure_value_or_evaluable(converter, v)
    )
    converter.register_structure_hook(Template, lambda v, t: structure_template(v))
    converter.register_structure_hook(Expression, lambda v, t: structure_expression(v))
    converter.register_structure_hook_func(
        lambda cls: cls is Evaluable, lambda v, t: structure_expression(v)
    )
    converter.register_structure_hook(
        LogicExpressions, lambda v, t: structure_logic_expressions(converter, v)
    )

    converter.register_unstructure_hook(Template, unstructure_template)
    converter.register_unstructure_hook(Expression, unstructure_expression)
    converter.register_unstructure_hook(
        LogicAnd, lambda v: unstructure_and(converter, v)
    )
    converter.register_unstructure_hook(LogicOr, lambda v: unstructure_or(converter, v))
