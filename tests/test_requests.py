import pytest
from django.urls import reverse_lazy

from django_inertia import Inertia


def share_auth(request):
    if request.user.is_authenticated:
        return {"first_name": request.user.first_name}
    else:
        return False


@pytest.mark.django_db
class TestRequests:
    def test_can_share_user_globally(self, john_client, client):
        # make an unauthenticated request
        response = client.get(reverse_lazy("home"))
        output_props = response.context.get("page__").get("props")
        assert output_props.get("message") == "Hello World"
        assert not output_props.get("user")
        # make a request authenticated as John
        Inertia.share("user", share_auth)
        response = john_client.get(reverse_lazy("home"))
        output_props = response.context.get("page__").get("props")
        assert output_props.get("message") == "Hello World"
        assert output_props.get("user") == {"first_name": "John"}

        Inertia().flush_shared()

    def test_template_contains_view_data(self, client):
        response = client.get(reverse_lazy("home.extra_data"))
        output_props = response.context.get("page__").get("props")
        assert output_props.get("message") == "Hello World"
        assert response.context['app_name'] == "Django Inertia"
        assert response.context['app_version'] == "1.0"
