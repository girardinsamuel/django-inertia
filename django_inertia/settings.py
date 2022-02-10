from django.conf import settings as django_settings

__all__ = ["settings"]


class LazySettings:
    INERTIA_ROOT_VIEW = "app.html"

    def __getattribute__(self, name):
        try:
            return getattr(django_settings, name)
        except AttributeError:
            return super().__getattribute__(name)


settings = LazySettings()
