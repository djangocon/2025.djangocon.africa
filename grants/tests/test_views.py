import pytest
from django.test import RequestFactory, override_settings
from django.urls import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from grants.views import parse_budget, request_code, verify_code
from grants.models import GrantApplication, VerificationCode
from django.utils import timezone
from datetime import timedelta


# Fixture for RequestFactory with messages support
@pytest.fixture
def rf():
    factory = RequestFactory()
    return factory


@pytest.fixture
def request_with_messages(rf):
    def _request(method, url, data=None):
        request = getattr(rf, method.lower())(url, data or {})
        setattr(request, "session", {})
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        return request

    return _request


# Fixture for a grant application
@pytest.fixture
def grant_application(db):
    return GrantApplication.objects.create(
        email="test@example.com",
        full_name="Test Applicant",
        timestamp=timezone.now(),
        ticket_only="YES",
        grant_type="FULL",
        budget_details="Item 1: $100\nItem 2: $200\nTotal: $300",
        status="PENDING",
    )


# Fixture for a verification code
@pytest.fixture
def verification_code(db, grant_application):
    return VerificationCode.objects.create(
        email=grant_application.email,
        code="123456",
        expires_at=timezone.now() + timedelta(minutes=10),
    )


# Tests for parse_budget
def test_parse_budget_empty():
    result = parse_budget("")
    assert result == {"details": ""}


def test_parse_budget_only_details():
    budget_text = "Item 1: $100\nItem 2: $200"
    result = parse_budget(budget_text)
    assert result == {"details": "Item 1: $100\nItem 2: $200"}


def test_parse_budget_with_total():
    budget_text = "Item 1: $100\nTotal: $300"
    result = parse_budget(budget_text)
    assert result == {"details": "Item 1: $100", "total_amount": "$300.00"}


def test_parse_budget_with_total_no_decimal():
    budget_text = "Item 1: $100\nTotal: 300"
    result = parse_budget(budget_text)
    assert result == {"details": "Item 1: $100", "total_amount": "$300.00"}


def test_parse_budget_with_total_dollar_after():
    budget_text = "Item 1: $100\nTotal: 300$"
    result = parse_budget(budget_text)
    assert result == {"details": "Item 1: $100", "total_amount": "$300.00"}


def test_parse_budget_with_commas():
    budget_text = "Item 1: $1,000\nTotal: $3,000"
    result = parse_budget(budget_text)
    assert result == {"details": "Item 1: $1000", "total_amount": "$3000.00"}


# Tests for request_code
def test_request_code_get(request_with_messages):
    request = request_with_messages("get", reverse("request_code"))
    response = request_code(request)
    assert response.status_code == 200
    assert b"email" in response.content.lower()


@pytest.mark.django_db
@override_settings(
    DEFAULT_FROM_EMAIL="from@example.com",
    DEFAULT_FROM_NAME="DjangoCon",
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
def test_request_code_post_empty_email(request_with_messages):
    request = request_with_messages("post", reverse("request_code"), {"email": ""})
    response = request_code(request)
    assert response.status_code == 200
    assert b"please enter a valid email" in response.content.lower()
    messages = list(request._messages)
    assert len(messages) == 1
    assert str(messages[0]) == "Please enter a valid email."


@pytest.mark.django_db
@override_settings(
    DEFAULT_FROM_EMAIL="from@example.com",
    DEFAULT_FROM_NAME="DjangoCon",
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
def test_request_code_post_nonexistent_email(request_with_messages):
    request = request_with_messages(
        "post", reverse("request_code"), {"email": "test@example.com"}
    )
    response = request_code(request)
    assert response.status_code == 200
    assert b"email not found" in response.content.lower()
    messages = list(request._messages)
    assert len(messages) == 1
    assert str(messages[0]) == "Email not found in our database."


@override_settings(
    DEFAULT_FROM_EMAIL="from@example.com",
    DEFAULT_FROM_NAME="DjangoCon",
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
def test_request_code_post_success(mocker, request_with_messages, grant_application):
    mock_send_email = mocker.patch("grants.views.send_email", return_value=True)
    request = request_with_messages(
        "post", reverse("request_code"), {"email": "test@example.com"}
    )
    response = request_code(request)
    assert mock_send_email.called
    assert response.status_code == 302
    assert response.url == reverse("verify_code", kwargs={"email": "test@example.com"})
    messages = list(request._messages)
    assert len(messages) == 1
    assert str(messages[0]) == "Verification code sent to your email."
    assert VerificationCode.objects.filter(email="test@example.com").exists()
    mocker.stopall()


@override_settings(
    DEFAULT_FROM_EMAIL="from@example.com",
    DEFAULT_FROM_NAME="DjangoCon",
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
def test_request_code_post_email_failure(
    mocker, request_with_messages, grant_application
):
    mock_send_email = mocker.patch("grants.views.send_email", return_value=False)
    request = request_with_messages(
        "post", reverse("request_code"), {"email": "test@example.com"}
    )
    response = request_code(request)
    assert mock_send_email.called
    assert response.status_code == 200
    assert b"failed to send email" in response.content.lower()
    messages = list(request._messages)
    assert len(messages) == 1
    assert str(messages[0]) == "Failed to send email. Please try again."
    mocker.stopall()


# Tests for verify_code
@pytest.mark.django_db
def test_verify_code_invalid_email(request_with_messages):
    request = request_with_messages(
        "get", reverse("verify_code", kwargs={"email": "test@example.com"})
    )
    response = verify_code(request, email="test@example.com")
    assert response.status_code == 302
    assert response.url == reverse("request_code")
    messages = list(request._messages)
    assert len(messages) == 1
    assert str(messages[0]) == "Email not found in our database."


def test_verify_code_get(request_with_messages, grant_application):
    request = request_with_messages(
        "get", reverse("verify_code", kwargs={"email": "test@example.com"})
    )
    response = verify_code(request, email="test@example.com")
    assert response.status_code == 200
    assert b"verification code" in response.content.lower()


def test_verify_code_post_valid_code(
    request_with_messages, grant_application, verification_code
):
    request = request_with_messages(
        "post",
        reverse("verify_code", kwargs={"email": "test@example.com"}),
        {"code": "123456"},
    )
    response = verify_code(request, email="test@example.com")
    assert response.status_code == 200
    assert b"grant application" in response.content.lower()
    assert not VerificationCode.objects.filter(email="test@example.com").exists()


def test_verify_code_post_invalid_code(request_with_messages, grant_application):
    request = request_with_messages(
        "post",
        reverse("verify_code", kwargs={"email": "test@example.com"}),
        {"code": "999999"},
    )
    response = verify_code(request, email="test@example.com")
    assert response.status_code == 200
    assert b"invalid or expired code" in response.content.lower()
    messages = list(request._messages)
    assert len(messages) == 1
    assert str(messages[0]) == "Invalid or expired code."
    assert not VerificationCode.objects.filter(email="test@example.com").exists()


def test_verify_code_post_expired_code(
    request_with_messages, grant_application, verification_code
):
    verification_code.expires_at = timezone.now() - timedelta(minutes=1)
    verification_code.save()
    request = request_with_messages(
        "post",
        reverse("verify_code", kwargs={"email": "test@example.com"}),
        {"code": "123456"},
    )
    response = verify_code(request, email="test@example.com")
    assert response.status_code == 200
    assert b"invalid or expired code" in response.content.lower()
    messages = list(request._messages)
    assert len(messages) == 1
    assert str(messages[0]) == "Invalid or expired code."
    assert not VerificationCode.objects.filter(email="test@example.com").exists()
