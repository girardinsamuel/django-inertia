from django.test import TestCase

from django_inertia import Inertia


class TestInertia(TestCase):
    def setUp(self) -> None:
        super().setUp()
        Inertia().flush_shared()

    def test_script_rendered(self):
        pass

    def test_render(self):
        # check props, components, version, url are here
        pass

    def test_location(self):
        response = Inertia.location("https://github.com")
        self.assertEqual(409, response.status_code)
        self.assertEqual(response.headers.get("X-Inertia-Location"), "https://github.com")

    # @override_settings(INERTIA_ROOT_VIEW="global_test.html")
    # def test_overriding_root_view(self):
    #     assert Inertia().options.get("root_view") == "global_test.html"
