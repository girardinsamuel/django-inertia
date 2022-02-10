import uuid

from django.http import HttpResponse, HttpResponseRedirect
from django.test import RequestFactory, TestCase

from django_inertia.core import Inertia
from django_inertia.middleware import InertiaMiddleware


class TestInertiaMiddleware(TestCase):
    """Test indenpendently middleware flow"""

    def setUp(self) -> None:
        super().setUp()
        self.middleware = InertiaMiddleware(lambda x: HttpResponse())
        self.request = RequestFactory().get("/")
        self.request.session = {}

    def test_initiate_location_if_version_changed(self):
        self.request.headers = {
            "X-Inertia": "true",
            "X-Requested-With": "XMLHttpRequest",
            "X-Inertia-Version": uuid.uuid4(),
        }
        response = self.middleware(self.request)
        assert response.status_code == 409
        assert response.headers.get("X-Inertia-Location", "/")

    def test_redirect_303_for_put_patch_delete_redirect_requests(self):
        middleware = InertiaMiddleware(lambda x: HttpResponseRedirect(redirect_to="/home"))

        request = RequestFactory().put("/users/1")
        request.session = {}
        response = middleware(request)
        assert response.status_code == 303

        request = RequestFactory().patch("/users/1")
        request.session = {}
        response = middleware(request)
        assert response.status_code == 303

        request = RequestFactory().delete("/users/1")
        request.session = {}
        response = middleware(request)
        assert response.status_code == 303

    def test_that_inertia_version_is_appended_if_no_version(self):
        Inertia.version("")
        self.request.headers = {
            "X-Inertia": "true",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.middleware(self.request)
        assert Inertia.get_version() == "1"
