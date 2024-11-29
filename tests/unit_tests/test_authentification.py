import pytest
from django.core import mail
from django.test import Client
from pytest_django.asserts import assertRedirects, assertTemplateUsed
from custom_auth.models import User

client = Client()

@pytest.fixture
def user_fixture(db, django_user_model):
    default_user = django_user_model.objects.create(
        first_name="Alice",
        last_name="Nolastname",
        email="alice@wonderland.com",
        password="nfpt30x49q2obt9"
    )
    return default_user

@pytest.mark.django_db
def test_register():
    response = client.post(
        "/accounts/register/",
        dict(email="rabbit.white@wonderland.com",
        last_name="Rabbit", first_name="White",
        password1="FNEYghfr",
        password2="FNEYghfr"),
        format="text/html")
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_register_page():
    response = client.get("/accounts/signup/")
    assert response.status_code ==  200
    assertTemplateUsed(response, "account/signup.html")

@pytest.mark.django_db
def test_valid_template_for_forgotten_password():
    response = client.get("/accounts/password/reset/")
    assertTemplateUsed(response, "account/password_reset.html")


@pytest.mark.django_db
def test_valid_email_sending_for_forgotten_password(user_fixture):
    u = user_fixture
    response = client.post(
        "/accounts/password/reset/",
        dict(email=u.email),
        format="text/html"
    )
    assertRedirects(
        response,
        "/accounts/password/reset/done/",
        status_code=302,
        target_status_code=200,
        fetch_redirect_response=True
    )
    assert mail.outbox[0].to == [u.email]
    assert len(mail.outbox) ==  1



def test_valid_url_to_reset_password(user_fixture):
    u = User.objects.get(email = "alice@wonderland.com")
    client.post("/accounts/password/reset/",
                                dict(email=u.email),
                               format="text/html")
    email_lines = mail.outbox[0].body.splitlines()
    url = email_lines[6]
    re = client.post(
        url,
        dict(password1="FNEYghfr",password2="FNEYghfr"),
        format="text/html")
    assert re.status_code == 200
