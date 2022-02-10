def assert_component(response, component):
    assert (
        response.context["page"]["component"] == component
    ), f"Asserted {component}, got {response.context['page']['component']}"


def assert_props(response, key, value=None):
    props = response.context["page"]["props"]
    assert key in props
    if value:
        assert props.get(key, None) == value
