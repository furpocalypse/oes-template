"""Template module."""
from typing import Any

import jinja2.environment
from attrs import Factory, field, frozen

from oes.template.env import get_jinja2_env


def _compile(tmpl):
    env = get_jinja2_env()
    return env.from_string(tmpl.source)


@frozen(repr=False)
class Template:
    """Jinja2 template."""

    source: str
    """The template source."""

    _compiled: jinja2.Template = field(
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

    def render(self, **context: Any) -> str:
        """Render the template."""
        return self._compiled.render(**context)


def structure_template(v: object) -> Template:
    if isinstance(v, str):
        return Template(v)
    else:
        raise TypeError(f"Invalid template: {v!r}")


def unstructure_template(v: Template) -> str:
    return v.source
