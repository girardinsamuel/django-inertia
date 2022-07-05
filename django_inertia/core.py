import html
import typing
from inspect import signature

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render
from dotty_dict import dotty

from .props import LazyProp, StaticProp
from .settings import settings


def load_callable_props(d: dict, request: HttpRequest):
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
    _instance: typing.Optional['Inertia'] = None
    shared_props: dict = {}
    rendered_template: str = ""
    _version: str = ""
    options: dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Inertia, cls).__new__(cls)
            # Put any initialization here.
            cls._instance.options = {
                "root_view": settings.INERTIA_ROOT_VIEW,
                "page_context": settings.INERTIA_PAGE_CONTEXT,
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
    def render(cls, request: HttpRequest, component: str, props: typing.Optional[dict] = None,
               view_data: typing.Optional[dict] = None, custom_root_view: typing.Optional[str] = None):
        if view_data is None:
            view_data = {}
        if props is None:
            props = {}
        self = cls()
        page_data = self.get_page_data(request, component, props=props)

        if request.headers.get("X-Inertia", False):
            response = JsonResponse(page_data)
            response["X-Inertia"] = True
            response["Vary"] = "Accept"
            return response

        template = custom_root_view if custom_root_view else self.options.get("root_view")
        page_context = self.options.get('page_context')

        page_data = {page_context: page_data} if not view_data else \
            {**view_data, **{page_context: page_data}}

        return render(
            request,
            template,
            page_data,
        )

    @classmethod
    def location(cls, url: str):
        response = HttpResponse(status=409)
        response["X-Inertia-Location"] = url
        return response

    @staticmethod
    def lazy(callable: typing.Callable):
        return LazyProp(callable)

    @staticmethod
    def static(value: typing.Any):
        return StaticProp(value)

    def get_page_data(self, request: HttpRequest, component: str, props: dict):
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

    def get_shared_props(self, key: typing.Optional[str] = None, default: typing.Optional[str] = None):
        """Get all Inertia shared props or the one with the given key."""
        if key:
            return dotty(self.shared_props, key, default)
        else:
            return self.shared_props

    @classmethod
    def version(cls, version: typing.Any):
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
    def share(cls, key: typing.Union[str, dict], value: typing.Any = None):
        self = cls()
        if isinstance(key, dict):
            self.shared_props = {**self.shared_props, **key}
        else:
            self.shared_props.update({key: value})
        return self

    def flush_shared(self):
        self.shared_props = {}

    def get_props_to_use(self, request: HttpRequest, all_props: dict, component: str):
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

    def get_component(self, component: str):
        # TODO: check if escaping before here is needed
        return html.escape(component)
