"""Default Jinja2 environment."""
from contextvars import ContextVar

import jinja2
from jinja2.sandbox import ImmutableSandboxedEnvironment

default_jinja2_env = ImmutableSandboxedEnvironment()
"""The default Jinja2 environment."""

jinja2_env_context: ContextVar[jinja2.Environment] = ContextVar(
    "jinja2_env_context", default=default_jinja2_env
)
"""The context var for the configured Jinja2 environment."""


def get_jinja2_env() -> jinja2.Environment:
    """Get the currently configured Jinja2 environment."""
    return jinja2_env_context.get()
