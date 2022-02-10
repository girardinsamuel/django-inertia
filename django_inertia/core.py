import html
from inspect import signature
from typing import Any, Callable

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from dotty_dict import dotty

from .props import LazyProp, StaticProp
from .settings import settings


def load_callable_props(d, request):
    for k, v in d.items():
        if isinstance(v, dict):
            load_callable_props(v, request)
        elif callable(v):
            # evaluate prop and pass request if prop accept it
            if len(signature(v).parameters) > 0:
                d[k] = v(request)
            else:
                d[k] = v()
        elif isinstance(v, LazyProp):
            if len(signature(v.callable).parameters) > 0:
                d[k] = v(request)
            else:
                d[k] = v()
        elif isinstance(v, StaticProp):
            d[k] = v()


# Straightforward implementation of the Singleton Pattern
class Inertia(object):
    _instance = None
    shared_props = {}
    rendered_template = ""
    _version = ""

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Inertia, cls).__new__(cls)
            # Put any initialization here.
            cls._instance.options = {
                "root_view": settings.INERTIA_ROOT_VIEW,
            }
            cls._instance.check_config()

        return cls._instance

    def check_config(self):
        if not self.options.get("root_view"):
            raise ImproperlyConfigured(
                "No Inertia template found. Either set INERTIA_ROOT_VIEW"
                "in settings.py or pass template parameter."
            )

    @classmethod
    def render(cls, request, component, props={}, custom_root_view=None):
        self = cls()
        page_data = self.get_page_data(request, component, props=props)

        if request.headers.get("X-Inertia", False):
            response = JsonResponse(page_data)
            response["X-Inertia"] = True
            response["Vary"] = "Accept"
            return response
        template = custom_root_view if custom_root_view else self.options.get("root_view")
        return render(
            request,
            template,
            {"page": page_data},
        )

    @classmethod
    def location(cls, url):
        response = HttpResponse(status=409)
        response["X-Inertia-Location"] = url
        return response

    @staticmethod
    def lazy(callable: Callable):
        return LazyProp(callable)

    @staticmethod
    def static(value: Any):
        return StaticProp(value)

    def get_page_data(self, request, component, props):
        # merge shared props with page props, shared props keys takes precedence
        all_props = {**props, **self.get_shared_props()}
        # get props to use here if partial loading is requested
        props = self.get_props_to_use(request, all_props, component)
        # finally lazy load props and make request available to props being lazy loaded
        load_callable_props(props, request)

        page_data = {
            "component": self.get_component(component),
            "props": props,
            "url": request.get_full_path_info(),
            "version": self.get_version(),
        }

        return page_data

    def get_shared_props(self, key=None, default=None):
        """Get all Inertia shared props or the one with the given key."""
        if key:
            return dotty(self.shared_props, key, default)
        else:
            return self.shared_props

    @classmethod
    def version(cls, version):
        self = cls()
        self._version = version
        return self

    @classmethod
    def get_version(cls):
        self = cls()
        if callable(self._version):
            version = self._version()
        else:
            version = self._version
        return str(version)

    @classmethod
    def share(cls, key, value=None):
        self = cls()
        if isinstance(key, dict):
            self.shared_props = {**self.shared_props, **key}
        else:
            self.shared_props.update({key: value})
        return self

    def flush_shared(self):
        self.shared_props = {}

    def get_props_to_use(self, request, all_props, component):
        """Get props to return to the page:
        - when partial reload, required return 'only' props
        - add adapter props along view props (errors, message, auth ...)"""

        # partial reload feature
        only_props_header = request.headers.get("X-Inertia-Partial-Data")
        partial_component_header = request.headers.get("X-Inertia-Partial-Component") or {
            "name": ""
        }
        is_partial = only_props_header and partial_component_header == component
        props = {}

        if is_partial:
            only_props = only_props_header
            for key in all_props:
                # always load static props
                if key in only_props or isinstance(all_props[key], StaticProp):
                    props.update({key: all_props[key]})
        else:
            for prop_key, value in all_props.items():
                if not isinstance(value, LazyProp):
                    props.update({prop_key: value})

        return props

    def get_component(self, component):
        # TODO: check if escaping before here is needed
        return html.escape(component)
