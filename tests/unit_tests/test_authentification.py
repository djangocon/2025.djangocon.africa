import pytest
from django.core import mail
from pytest_django.asserts import assertRedirects, assertTemplateUsed


@pytest.fixture
def user(db, django_user_model):
    return django_user_model.objects.create(
        first_name="Alice",
        last_name="Nolastname",
        email="alice@wonderland.com",
        password="nfpt30x49q2obt9"
    )


@pytest.mark.django_db
def test_register(client):
    response = client.post(
        "/accounts/signup/",
        dict(
            email="rabbit.white@wonderland.com",
            last_name="Rabbit",
            first_name="White",
            password1="FNEYghfr",
            password2="FNEYghfr",
        ),
        format="text/html",
    )
    assertRedirects(
        response,
        "/en/accounts/confirm-email/",
        status_code=302,
        target_status_code=200,
        fetch_redirect_response=True,
    )


@pytest.mark.django_db
def test_get_register_page(client):
    response = client.get("/accounts/signup/")
    assert response.status_code == 200
    assertTemplateUsed(response, "account/signup.html")


@pytest.mark.django_db
def test_valid_template_for_forgotten_password(client):
    response = client.get("/accounts/password/reset/")
    assertTemplateUsed(response, "account/password_reset.html")


@pytest.mark.django_db
def test_valid_email_sending_for_forgotten_password(user, client):
    response = client.post(
        "/accounts/password/reset/",
        dict(email=user.email),
        format="text/html",
    )
    assertRedirects(
        response,
        "/en/accounts/password/reset/done/",
        status_code=302,
        target_status_code=200,
        fetch_redirect_response=True,
    )
    assert mail.outbox[0].to == [user.email]
    assert len(mail.outbox) == 1


def test_valid_url_to_reset_password(user, client):
    client.post(
        "/accounts/password/reset/",
        dict(email=user.email),
        format="text/html",
    )
    email_lines = mail.outbox[0].body.splitlines()
    re = client.post(
        "/accounts/password/reset/",
        dict(password1="FNEYghfr", password2="FNEYghfr"),
        format="text/html",
    )
    assert re.status_code == 200
