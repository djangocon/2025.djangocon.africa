import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from grants.models import GrantApplication, VerificationCode
from django.contrib.messages import get_messages

from grants.views import parse_budget

pytestmark = pytest.mark.django_db  # Enable database access for all tests


# Fixture to create a GrantApplication
@pytest.fixture
def grant_application():
    return GrantApplication.objects.create(
        timestamp=timezone.now(),
        full_name="Test Applicant",
        email="test@example.com",
        ticket_only="YES",
        grant_type="FULL",
        budget_details="Travel: $500\nAccommodation: $300\nTotal: $800",
        status="PENDING",
    )


# Fixture to create a VerificationCode
@pytest.fixture
def verification_code(grant_application):
    return VerificationCode.objects.create(
        email=grant_application.email,
        code="123456",
        expires_at=timezone.now() + timedelta(minutes=10),
    )

# Tests for request_code
def test_request_code_valid_email(mocker, client, grant_application):
    mock_send_email = mocker.patch("grants.views.send_email", return_value=True)
    print("Mock applied (valid_email):", mock_send_email)  # Debug
    response = client.post(
        reverse("request_code"),
        {"email": grant_application.email},
        HTTP_ACCEPT_LANGUAGE="en",
    )
    print("Response status (valid_email):", response.status_code)  # Debug
    assert response.status_code == 302
    assert response.url == reverse(
        "verify_code", kwargs={"email": grant_application.email}
    )
    assert VerificationCode.objects.filter(email=grant_application.email).exists()
    verification_code = VerificationCode.objects.get(email=grant_application.email)
    assert len(verification_code.code) == 6
    assert verification_code.code.isdigit()
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == "Verification code sent to your email."


def test_request_code_invalid_email(client):
    response = client.post(
        reverse("request_code"), {"email": ""}, HTTP_ACCEPT_LANGUAGE="en"
    )
    assert response.status_code == 200
    assert "grants/request_code.html" in [t.name for t in response.templates]
    assert not VerificationCode.objects.filter(email="").exists()
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == "Please enter a valid email."


def test_request_code_nonexistent_email(client):
    response = client.post(
        reverse("request_code"),
        {"email": "nonexistent@example.com"},
        HTTP_ACCEPT_LANGUAGE="en",
    )
    assert response.status_code == 200
    assert "grants/request_code.html" in [t.name for t in response.templates]
    assert not VerificationCode.objects.filter(email="nonexistent@example.com").exists()
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == "Email not found in our database."


def test_request_code_email_failure(mocker, client, grant_application):
    mock_send_email = mocker.patch("grants.views.send_email", return_value=False)
    print("Mock applied (email_failure):", mock_send_email)  # Debug
    response = client.post(
        reverse("request_code"),
        {"email": grant_application.email},
        HTTP_ACCEPT_LANGUAGE="en",
    )
    print("Response status (email_failure):", response.status_code)  # Debug
    assert response.status_code == 200
    assert "grants/request_code.html" in [t.name for t in response.templates]
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == "Failed to send email. Please try again."


# Tests for verify_code
def test_verify_code_valid_code(client, verification_code, grant_application):
    response = client.post(
        reverse("verify_code", kwargs={"email": grant_application.email}),
        {"code": verification_code.code},
        HTTP_ACCEPT_LANGUAGE="en",
    )
    assert response.status_code == 200
    assert "grants/grant_status.html" in [t.name for t in response.templates]
    assert not VerificationCode.objects.filter(email=grant_application.email).exists()
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0


def test_verify_code_invalid_code(client, verification_code, grant_application):
    response = client.post(
        reverse("verify_code", kwargs={"email": grant_application.email}),
        {"code": "wrongcode"},
        HTTP_ACCEPT_LANGUAGE="en",
    )
    assert response.status_code == 200
    assert "grants/verify_code.html" in [t.name for t in response.templates]
    assert not VerificationCode.objects.filter(email=grant_application.email).exists()
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == "Invalid or expired code."


def test_verify_code_expired_code(client, grant_application):
    VerificationCode.objects.create(
        email=grant_application.email,
        code="123456",
        expires_at=timezone.now() - timedelta(minutes=1),
    )
    response = client.post(
        reverse("verify_code", kwargs={"email": grant_application.email}),
        {"code": "123456"},
        HTTP_ACCEPT_LANGUAGE="en",
    )
    assert response.status_code == 200
    assert "grants/verify_code.html" in [t.name for t in response.templates]
    assert not VerificationCode.objects.filter(email=grant_application.email).exists()
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == "Invalid or expired code."


def test_verify_code_nonexistent_application(client, verification_code):
    GrantApplication.objects.filter(email=verification_code.email).delete()
    response = client.post(
        reverse("verify_code", kwargs={"email": verification_code.email}),
        {"code": verification_code.code},
        HTTP_ACCEPT_LANGUAGE="en",
    )
    assert response.status_code == 302
    assert response.url == reverse("request_code")
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == "Email not found in our database."


def test_verify_code_get_request(client, grant_application):
    response = client.get(
        reverse("verify_code", kwargs={"email": grant_application.email}),
        HTTP_ACCEPT_LANGUAGE="en",
    )
    assert response.status_code == 200
    assert "grants/verify_code.html" in [t.name for t in response.templates]
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0
