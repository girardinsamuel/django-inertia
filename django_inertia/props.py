from typing import Any, Callable


class LazyProp:
    """Prop that will never be loaded the first time but can be loaded during partial reloads."""

    def __init__(self, callable_arg: Callable):
        self.callable = callable_arg

    def __call__(self, *args):
        return self.callable(*args)


class StaticProp:
    """Prop that will always be loaded even during partial reloads when not present in only.
    Can be useful to always share errors for example.
    As they are always loaded, a callable is not necessary so this takes a static value.
    """

    def __init__(self, value: Any):
        self.value = value

    def __call__(self, *args):
        return self.value
