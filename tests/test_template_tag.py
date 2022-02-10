from django.template import Context, Template
from django.test import TestCase


class TestInertiaTemplateTag(TestCase):
    def test_rendering_inertia_tag(self):
        rendered = Template("{% load inertia_tags %} {% inertia %}").render(
            Context(
                {
                    "page": {
                        "component": "Index",
                        "url": "/",
                        "props": {"message": "Hello"},
                        "version": "1",
                    }
                }
            )
        )
        assert 'id="app"' in rendered
        assert "component" in rendered
        assert "props" in rendered
        assert "version" in rendered
        assert "url" in rendered
        assert "message" in rendered

    def test_can_change_app_id(self):
        rendered = Template("{% load inertia_tags %} {% inertia 'my_app' %}").render(
            Context(
                {
                    "page": {
                        "component": "Index",
                        "url": "/",
                        "props": {"message": "Hello"},
                        "version": "1",
                    }
                }
            )
        )
        assert 'id="my_app"' in rendered
