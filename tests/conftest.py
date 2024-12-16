import pytest

from custom_auth.models import User


@pytest.fixture
def user(db, django_user_model):
    return django_user_model.objects.create(
        first_name="Alice",
        last_name="Nolastname",
        email="alice@wonderland.com",
        password="nfpt30x49q2obt9"
    )

