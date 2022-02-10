import pytest
from django.contrib.auth import get_user_model
from django.test import Client


@pytest.fixture()
def john(db):
    return get_user_model().objects.create(
        username="john", first_name="John", last_name="Doe", email="john.doe@django.org"
    )


@pytest.fixture()
def john_client(john):
    client = Client()
    client.force_login(john)
    return client
