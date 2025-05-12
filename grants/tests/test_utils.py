import pytest
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from grants.utils.email import send_email

# Fixture to temporarily modify settings.EMAIL_BACKEND
@pytest.fixture
def mock_settings():
    original_backend = getattr(settings, "EMAIL_BACKEND", None)
    yield settings
    settings.EMAIL_BACKEND = original_backend

# Test console backend
def test_send_email_console_success(mocker, mock_settings):
    # Arrange
    mock_settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    mock_email = mocker.patch.object(EmailMultiAlternatives, "send", return_value=None)
    mock_logger = mocker.patch("grants.utils.email.logger")  # Mock module-level logger

    # Act
    result = send_email(
        subject="Test Subject",
        text_content="Test Text",
        html_content="<p>Test HTML</p>",
        from_email="sender@example.com",
        from_name="Sender",
        to_email="recipient@example.com",
        to_name="Recipient",
    )

    # Assert
    assert result is True
    mock_email.assert_called_once()
    mock_logger.info.assert_called_once_with(
        "Email sent to recipient@example.com via console backend"
    )

def test_send_email_console_failure(mocker, mock_settings):
    # Arrange
    mock_settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    mock_email = mocker.patch.object(
        EmailMultiAlternatives, "send", side_effect=Exception("Send failed")
    )
    mock_logger = mocker.patch("grants.utils.email.logger")

    # Act
    result = send_email(
        subject="Test Subject",
        text_content="Test Text",
        html_content="<p>Test HTML</p>",
        from_email="sender@example.com",
        from_name="Sender",
        to_email="recipient@example.com",
    )

    # Assert
    assert result is False
    mock_email.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Error sending email via console backend: Send failed"
    )

# Test Mailjet backend
def test_send_email_mailjet_success(mocker, mock_settings):
    # Arrange
    mock_settings.EMAIL_BACKEND = "mailjet"
    mock_config = mocker.patch("grants.utils.email.config")
    mock_config.side_effect = lambda key: {
        "MAILJET_API_KEY": "api_key",
        "MAILJET_SECRET_KEY": "secret_key",
    }[key]
    # Mock Client without autospec
    mock_mailjet = mocker.patch("grants.utils.email.Client")
    # Manually set up send.create
    mock_mailjet.return_value.send = mocker.MagicMock()
    mock_send = mock_mailjet.return_value.send.create
    mock_send.return_value.status_code = 200
    mock_send.return_value.json.return_value = {"Messages": [{"Status": "success"}]}
    mock_logger = mocker.patch("grants.utils.email.logger")

    # Act
    result = send_email(
        subject="Test Subject",
        text_content="Test Text",
        html_content="<p>Test HTML</p>",
        from_email="sender@example.com",
        from_name="Sender",
        to_email="recipient@example.com",
        to_name="Recipient",
    )


    # Assert
    assert mock_mailjet.called, "Mailjet Client was not called"
    assert mock_send.called, "Mailjet send.create was not called"
    assert result is True
    mock_send.assert_called_once_with(
        data={
            "Messages": [
                {
                    "From": {"Email": "sender@example.com", "Name": "Sender"},
                    "To": [{"Email": "recipient@example.com", "Name": "Recipient"}],
                    "Subject": "Test Subject",
                    "TextPart": "Test Text",
                    "HTMLPart": "<p>Test HTML</p>",
                }
            ]
        }
    )
    mock_logger.info.assert_called_once_with(
        "Mailjet response: Status=200, Data={'Messages': [{'Status': 'success'}]}"
    )

def test_send_email_mailjet_failure_status_code(mocker, mock_settings):
    mock_settings.EMAIL_BACKEND = "mailjet"
    mock_config = mocker.patch("grants.utils.email.config")
    mock_config.side_effect = lambda key: {
        "MAILJET_API_KEY": "api_key",
        "MAILJET_SECRET_KEY": "secret_key",
    }[key]
    mock_mailjet = mocker.patch("grants.utils.email.Client")
    mock_mailjet.return_value.send = mocker.MagicMock()
    mock_send = mock_mailjet.return_value.send.create
    mock_send.return_value.status_code = 400
    mock_send.return_value.json.return_value = {"Error": "Bad request"}
    mock_logger = mocker.patch("grants.utils.email.logger")

    result = send_email(
        subject="Test Subject",
        text_content="Test Text",
        html_content="<p>Test HTML</p>",
        from_email="sender@example.com",
        from_name="Sender",
        to_email="recipient@example.com",
    )


    assert result is False
    mock_send.assert_called_once_with(
        data={
            "Messages": [
                {
                    "From": {"Email": "sender@example.com", "Name": "Sender"},
                    "To": [{"Email": "recipient@example.com", "Name": ""}],
                    "Subject": "Test Subject",
                    "TextPart": "Test Text",
                    "HTMLPart": "<p>Test HTML</p>",
                }
            ]
        }
    )
    mock_logger.error.assert_called_once_with(
        "Mailjet failed: Status=400, Data={'Error': 'Bad request'}"
    )


def test_send_email_mailjet_exception(mocker, mock_settings):
    mock_settings.EMAIL_BACKEND = "mailjet"
    mock_config = mocker.patch("grants.utils.email.config")
    mock_config.side_effect = lambda key: {
        "MAILJET_API_KEY": "api_key",
        "MAILJET_SECRET_KEY": "secret_key",
    }[key]
    mock_mailjet = mocker.patch("grants.utils.email.Client")
    mock_send = mock_mailjet.return_value.send.create
    mock_send.side_effect = Exception("API error")
    mock_logger = mocker.patch("grants.utils.email.logger")

    result = send_email(
        subject="Test Subject",
        text_content="Test Text",
        html_content="<p>Test HTML</p>",
        from_email="sender@example.com",
        from_name="Sender",
        to_email="recipient@example.com",
    )

    assert result is False
    mock_logger.error.assert_called_once_with(
        "Error sending email via Mailjet: API error"
    )

# Test edge cases
def test_send_email_empty_to_email(mocker, mock_settings):
    # Arrange
    mock_settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    mock_email = mocker.patch.object(
        EmailMultiAlternatives, "send", side_effect=Exception("Invalid email")
    )
    mock_logger = mocker.patch("grants.utils.email.logger")

    # Act
    result = send_email(
        subject="Test Subject",
        text_content="Test Text",
        html_content="<p>Test HTML</p>",
        from_email="sender@example.com",
        from_name="Sender",
        to_email="",
    )

    # Assert
    assert result is False
    mock_email.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Error sending email via console backend: Invalid email"
    )
