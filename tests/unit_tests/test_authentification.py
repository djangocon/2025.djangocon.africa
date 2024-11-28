import pytest
from django.core import mail
from django.test import Client
from pytest_django.asserts import assertRedirects, assertTemplateUsed
from custom_auth.models import User
from custom_auth import utils

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

def test_send_registration_email():
   utils.send_registration_email(
       email="alice@wonderland.com",
       username ="alice")
   assert len(mail.outbox) == 1

@pytest.mark.django_db
def test_register():
    response = client.post(
        "/accounts/register/",
        dict(email="rabbit.white@wonderland.com",
        last_name="Rabbit", first_name="White",
        password1="FNEYghfr",
        password2="FNEYghfr"),
        format="text/html")
    assertRedirects(response, "/accounts/login/", status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_get_register_page():
    response = client.get("/accounts/register/")
    assert response.status_code ==  200
    assertTemplateUsed(response, "registration/register.html")

@pytest.mark.django_db
def test_valid_template_for_forgotten_password():
    response = client.get("/accounts/password_reset/")
    assertTemplateUsed(response, "registration/password_reset_form.html")


@pytest.mark.django_db
def test_valid_email_sending_for_forgotten_password(user_fixture):
    u = user_fixture
    response = client.post(
        "/accounts/password_reset/",
        dict(email=u.email),
        format="text/html"
    )
    assertRedirects(
        response,
        "/accounts/password_reset/done/",
        status_code=302,
        target_status_code=200,
        fetch_redirect_response=True
    )
    assert mail.outbox[0].to == [u.email]
    assert len(mail.outbox) ==  1



def test_valid_url_to_reset_password(user_fixture):
    u = User.objects.get(email = "alice@wonderland.com")
    client.post("/accounts/password_reset/",
                                dict(email=u.email),
                               format="text/html")
    email_lines = mail.outbox[0].body.splitlines()
    url = email_lines[5]
    response = client.get(url)
    assert response.status_code == 302
    re = client.post(
        response.url,
        dict(password1="FNEYghfr",password2="FNEYghfr"),
        format="text/html")
    assert re.status_code == 200
