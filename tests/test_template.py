import pytest

from oes.template.template import Template


@pytest.mark.parametrize(
    "src, context, value",
    [
        ("normal", {}, "normal"),
        ("{{ test }}", {"test": "text"}, "text"),
        ("{{ test }}", {}, ""),
    ],
)
def test_template(src, context, value):
    template = Template(src)
    res = template.render(**context)
    assert res == value
