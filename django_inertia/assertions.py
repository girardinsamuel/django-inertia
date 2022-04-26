from .core import Inertia


def assert_component(response, component):
    assert (
        response.context[Inertia.options.get('page_context')]["component"] == component
    ), f"Asserted {component}, " \
       f"got {response.context[Inertia.options.get('page_context')]['component']}"


def assert_props(response, key, value=None):
    props = response.context[Inertia.options.get("page_context")]["props"]
    assert key in props
    if value:
        assert props.get(key, None) == value
