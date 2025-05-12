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
        status="PENDING"
    )

# Fixture to create a VerificationCode
@pytest.fixture
def verification_code(grant_application):
    return VerificationCode.objects.create(
        email=grant_application.email,
        code="123456",
        expires_at=timezone.now() + timedelta(minutes=10)
    )


def test_empty_input():
    result = parse_budget("")
    assert result == {"details": ""}

def test_total_only():
    input_text = "Total Amount: 1500$"
    result = parse_budget(input_text)
    assert result == {
        "total_amount": "$1500.00",
        "details": ""
    }

def test_details_only():
    input_text = """• Flight (round‐trip): approximately $350
• Lodging: $50 per night × 5 nights = $250
• Visa: $0
• Ground Transportation: approximately $100
• Incidentals: approximately $100"""
    result = parse_budget(input_text)
    assert result == {
        "details": "• Flight (round‐trip): approximately $350\n• Lodging: $50 per night × 5 nights = $250\n• Visa: $0\n• Ground Transportation: approximately $100\n• Incidentals: approximately $100"
    }
    assert "total_amount" not in result

def test_total_and_details():
    input_text = """I will need a Total  of :  $891
Fight (round-trip): $831
Lodging -  $60
Visa - I do not need a visa
Ground Transportation - I will cover ground transportation"""
    result = parse_budget(input_text)
    assert result == {
        "total_amount": "$891.00",
        "details": "Fight (round-trip): $831\nLodging -  $60\nVisa - I do not need a visa\nGround Transportation - I will cover ground transportation"
    }

def test_decimal_total():
    input_text = """Total Amount: 2171.52
Flight (round-trip) : 1739$
Lodging - US$38.13 × 4 nights
(US$152.52)
Visa: 0$
Ground Transportation - 80$
miscellaneous- 200$"""
    result = parse_budget(input_text)
    assert result == {
        "total_amount": "$2171.52",
        "details": "Flight (round-trip) : 1739$\nLodging - US$38.13 × 4 nights\n(US$152.52)\nVisa: 0$\nGround Transportation - 80$\nmiscellaneous- 200$"
    }

def test_case_insensitivity():
    input_text = """TOTAL: $500
Item: $100"""
    result = parse_budget(input_text)
    assert result == {
        "total_amount": "$500.00",
        "details": "Item: $100"
    }

def test_extra_whitespace():
    input_text = """\n  Total: $1000  \n\nItem1: $500\n  Item2: $300  \n\n"""
    result = parse_budget(input_text)
    assert result == {
        "total_amount": "$1000.00",
        "details": "Item1: $500\nItem2: $300"
    }

def test_commas_in_total():
    input_text = """Total: 1,500$
Details: Some item"""
    result = parse_budget(input_text)
    assert result == {
        "total_amount": "$1500.00",
        "details": "Details: Some item"
    }

def test_total_line_excluded_from_details():
    input_text = """Line 1: $100
Total Amount: $300
Line 2: $200"""
    result = parse_budget(input_text)
    assert result == {
        "total_amount": "$300.00",
        "details": "Line 1: $100\nLine 2: $200"
    }

# Tests for request_code
def test_request_code_valid_email(mocker, client, grant_application):
    mock_send_email = mocker.patch("grants.views.send_email", return_value=True)
    print("Mock applied (valid_email):", mock_send_email)  # Debug
    response = client.post(
        reverse("request_code"),
        {"email": grant_application.email},
        HTTP_ACCEPT_LANGUAGE="en"
    )
    print("Response status (valid_email):", response.status_code)  # Debug
    assert response.status_code == 302
    assert response.url == reverse("verify_code", kwargs={"email": grant_application.email})
    assert VerificationCode.objects.filter(email=grant_application.email).exists()
    verification_code = VerificationCode.objects.get(email=grant_application.email)
    assert len(verification_code.code) == 6
    assert verification_code.code.isdigit()
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == "Verification code sent to your email."

def test_request_code_invalid_email(client):
    response = client.post(
        reverse("request_code"),
        {"email": ""},
        HTTP_ACCEPT_LANGUAGE="en"
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
        HTTP_ACCEPT_LANGUAGE="en"
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
        HTTP_ACCEPT_LANGUAGE="en"
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
        HTTP_ACCEPT_LANGUAGE="en"
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
        HTTP_ACCEPT_LANGUAGE="en"
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
        expires_at=timezone.now() - timedelta(minutes=1)
    )
    response = client.post(
        reverse("verify_code", kwargs={"email": grant_application.email}),
        {"code": "123456"},
        HTTP_ACCEPT_LANGUAGE="en"
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
        HTTP_ACCEPT_LANGUAGE="en"
    )
    assert response.status_code == 302
    assert response.url == reverse("request_code")
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == "Email not found in our database."

def test_verify_code_get_request(client, grant_application):
    response = client.get(
        reverse("verify_code", kwargs={"email": grant_application.email}),
        HTTP_ACCEPT_LANGUAGE="en"
    )
    assert response.status_code == 200
    assert "grants/verify_code.html" in [t.name for t in response.templates]
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0