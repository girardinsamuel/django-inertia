import json

from django.template import Context, Template
from django.test import TestCase


class TestInertiaTemplateTag(TestCase):
    def test_rendering_inertia_tag(self):
        rendered = Template("{% load inertia_tags %} {% inertia %}").render(
            Context(
                {
                    "page__": {
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
                    "page__": {
                        "component": "Index",
                        "url": "/",
                        "props": {"message": "Hello"},
                        "version": "1",
                    }
                }
            )
        )
        assert 'id="my_app"' in rendered

    def test_data_page_valid_json(self):
        rendered = Template("{% load inertia_tags %} {% inertia %}").render(
            Context(
                {
                    "page__": {
                        "component": "Index",
                        "url": "/",
                        "props": {"message": "Hello"},
                        "version": "1",
                    }
                }
            )
        )

        # Assert that a JSON-parsable string is found in the data-page attr
        json_parsable_context_string = (
            '{"component": "Index", "url": "/", "props": {"message": "Hello"}, "version": "1"}'
        )
        assert f"data-page='{json_parsable_context_string}'" in rendered

        # Assert that the data-page attr value is a valid JSON string
        assert type(json.loads(json_parsable_context_string)) == dict
