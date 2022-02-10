from django.urls import reverse_lazy

from django_inertia import Inertia


def share_auth(request):
    if request.user.is_authenticated:
        return {"first_name": request.user.first_name}
    else:
        return False


class TestRequests:
    def test_can_share_user_globally(self, john_client, client):
        # make an unauthenticated request
        response = client.get(reverse_lazy("home"))
        output_props = response.context.get("page").get("props")
        assert output_props.get("message") == "Hello World"
        assert not output_props.get("user")
        # make a request authenticated as John
        Inertia.share("user", share_auth)
        response = john_client.get(reverse_lazy("home"))
        output_props = response.context.get("page").get("props")
        assert output_props.get("message") == "Hello World"
        assert output_props.get("user") == {"first_name": "John"}

        Inertia().flush_shared()
