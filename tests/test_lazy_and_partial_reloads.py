from django.core.handlers.wsgi import WSGIRequest
from django.test import RequestFactory
from django.test.testcases import SimpleTestCase

from django_inertia import Inertia


class TestLazyAndPartialReloads(SimpleTestCase):
    def setUp(self):
        factory = RequestFactory()
        self.request = factory.get("/test-inertia")
        # for idempotent tests
        Inertia().flush_shared()

    def test_callable_prop_is_included_initially(self):
        props = {"normal": "value", "lazy": lambda r: "lazy_value"}
        response = Inertia.render(self.request, "Index", props)
        self.assertContains(response, "normal")
        self.assertContains(response, "lazy")

        self.request.headers = {
            "X-Inertia-Partial-Data": ["normal"],
            "X-Inertia-Partial-Component": "Index",
        }
        response = Inertia.render(self.request, "Index", props)
        self.assertContains(response, "normal")
        self.assertNotContains(response, "lazy")

    def test_lazy_prop_is_not_include_initially(self):
        props = {"normal": "value", "lazy": Inertia.lazy(lambda r: "lazy_value")}
        response = Inertia.render(self.request, "Index", props)
        self.assertContains(response, "normal")
        self.assertNotContains(response, "lazy")

        self.request.headers = {
            "X-Inertia-Partial-Data": ["lazy"],
            "X-Inertia-Partial-Component": "Index",
        }
        response = Inertia.render(self.request, "Index", props)
        self.assertContains(response, "lazy")
        self.assertNotContains(response, "normal")

    def test_lazy_or_callable_prop_receives_request(self):
        def my_callable(req):
            assert isinstance(req, WSGIRequest)
            return req.get_full_path()

        props = {"callable_prop": my_callable, "lazy_prop": Inertia.lazy(my_callable)}
        response = Inertia.render(self.request, "Index", props)
        self.assertContains(response, "/test-inertia")

    def test_can_share_globally_lazy_or_callable_props(self):
        Inertia.share(
            {"user": Inertia.lazy(lambda r: {"first_name": "John"}), "notifs": lambda r: []}
        )
        response = Inertia.render(self.request, "Index")
        self.assertNotContains(response, "user")
        self.assertContains(response, "notifs")

        self.request.headers = {
            "X-Inertia-Partial-Data": ["user", "notifs"],
            "X-Inertia-Partial-Component": "Index",
        }
        response = Inertia.render(self.request, "Index")
        self.assertContains(response, "user")
        self.assertContains(response, "notifs")

    def test_that_static_props_are_always_loaded(self):
        Inertia.share("errors", Inertia.static("Unknown error"))
        response = Inertia.render(self.request, "Index")
        self.assertContains(response, "errors")

        self.request.headers = {
            "X-Inertia-Partial-Data": ["message"],
            "X-Inertia-Partial-Component": "Index",
        }
        response = Inertia.render(self.request, "Index", {"message": "Hello"})
        self.assertContains(response, "message")
        self.assertContains(response, "errors")
