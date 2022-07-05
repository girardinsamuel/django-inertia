import typing

from .core import Inertia
from django.http import HttpResponse


def assert_component(response, component: str):
    assert (
        response.context[Inertia.options.get('page_context')]["component"] == component
    ), f"Asserted {component}, " \
       f"got {response.context[Inertia.options.get('page_context')]['component']}"


def assert_props(response, key: typing.Any, value: typing.Any = None):
    props = response.context[Inertia.options.get("page_context")]["props"]
    assert key in props
    if value:
        assert props.get(key, None) == value
