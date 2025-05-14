import pytest
from django.core.mail import EmailMultiAlternatives
from grants.utils.email import send_email


# Fixture for common email parameters
@pytest.fixture
def email_params():
    return {
        "subject": "Test Subject",
        "text_content": "This is a test email",
        "html_content": "<p>This is a test email</p>",
        "from_email": "sender@example.com",
        "from_name": "Sender Name",
        "to_email": "recipient@example.com",
        "to_name": "Recipient Name",
    }


# Console backend tests
def test_send_email_console_success(mocker, settings, email_params):
    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    mock_email = mocker.patch.object(EmailMultiAlternatives, "send", return_value=True)
    mock_logger = mocker.patch("grants.utils.email.logger")

    result = send_email(**email_params)

    assert result is True
    mock_email.assert_called_once()
    mock_logger.info.assert_called_once_with(
        "Email sent to recipient@example.com via console backend"
    )
    mock_logger.error.assert_not_called()


def test_send_email_console_exception(mocker, settings, email_params):
    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    mock_email = mocker.patch.object(
        EmailMultiAlternatives, "send", side_effect=Exception("Send failed")
    )
    mock_logger = mocker.patch("grants.utils.email.logger")

    result = send_email(**email_params)

    assert result is False
    mock_email.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Error sending email via console backend: Send failed"
    )
    mock_logger.info.assert_not_called()


def test_send_email_console_invalid_subject(mocker, settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    mock_email = mocker.patch.object(EmailMultiAlternatives, "send")
    mock_logger = mocker.patch("grants.utils.email.logger")

    result = send_email(
        subject="",
        text_content="Test Text",
        html_content="<p>Test HTML</p>",
        from_email="sender@example.com",
        from_name="Sender",
        to_email="recipient@example.com",
    )

    assert result is False
    mock_email.assert_not_called()
    mock_logger.info.assert_not_called()
    mock_logger.error.assert_not_called()


def test_send_email_console_invalid_to_email(mocker, settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    mock_email = mocker.patch.object(EmailMultiAlternatives, "send")
    mock_logger = mocker.patch("grants.utils.email.logger")

    result = send_email(
        subject="Test Subject",
        text_content="Test Text",
        html_content="<p>Test HTML</p>",
        from_email="sender@example.com",
        from_name="Sender",
        to_email="",
    )

    assert result is False
    mock_email.assert_not_called()
    mock_logger.info.assert_not_called()
    mock_logger.error.assert_not_called()


def test_send_email_console_invalid_text_content(mocker, settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    mock_email = mocker.patch.object(EmailMultiAlternatives, "send")
    mock_logger = mocker.patch("grants.utils.email.logger")

    result = send_email(
        subject="Test Subject",
        text_content="",
        html_content="<p>Test HTML</p>",
        from_email="sender@example.com",
        from_name="Sender",
        to_email="recipient@example.com",
    )

    assert result is False
    mock_email.assert_not_called()
    mock_logger.info.assert_not_called()
    mock_logger.error.assert_not_called()


# Mailjet backend tests
def test_send_email_mailjet_success(mocker, settings, email_params):
    settings.EMAIL_BACKEND = "mailjet"
    mock_response = mocker.MagicMock(
        status_code=200, json=mocker.MagicMock(return_value={"Messages": []})
    )
    mock_client = mocker.patch("grants.utils.email.Client")
    mock_client.return_value.send.create.return_value = mock_response
    mocker.patch("grants.utils.email.config", side_effect=lambda x: "dummy_value")
    mock_logger = mocker.patch("grants.utils.email.logger")

    result = send_email(**email_params)

    assert result is True
    mock_client.assert_called_once_with(
        auth=("dummy_value", "dummy_value"), version="v3.1"
    )
    mock_client.return_value.send.create.assert_called_once()
    mock_logger.info.assert_called_once_with(
        "Mailjet response: Status=200, Data={'Messages': []}"
    )
    mock_logger.error.assert_not_called()


def test_send_email_mailjet_failure(mocker, settings, email_params):
    settings.EMAIL_BACKEND = "mailjet"
    mock_response = mocker.MagicMock(
        status_code=400, json=mocker.MagicMock(return_value={"Error": "Bad request"})
    )
    mock_client = mocker.patch("grants.utils.email.Client")
    mock_client.return_value.send.create.return_value = mock_response
    mocker.patch("grants.utils.email.config", side_effect=lambda x: "dummy_value")
    mock_logger = mocker.patch("grants.utils.email.logger")

    result = send_email(**email_params)

    assert result is False
    mock_client.assert_called_once_with(
        auth=("dummy_value", "dummy_value"), version="v3.1"
    )
    mock_client.return_value.send.create.assert_called_once()
    mock_logger.error.assert_called_once_with(
        "Mailjet failed: Status=400, Data={'Error': 'Bad request'}"
    )
    mock_logger.info.assert_called_once()


def test_send_email_mailjet_exception(mocker, settings, email_params):
    settings.EMAIL_BACKEND = "mailjet"
    mock_client = mocker.patch(
        "grants.utils.email.Client", side_effect=Exception("API error")
    )
    mocker.patch("grants.utils.email.config", side_effect=lambda x: "dummy_value")
    mock_logger = mocker.patch("grants.utils.email.logger")

    result = send_email(**email_params)

    assert result is False
    mock_client.assert_called_once_with(
        auth=("dummy_value", "dummy_value"), version="v3.1"
    )
    mock_logger.error.assert_called_once_with(
        "Error sending email via Mailjet: API error"
    )
    mock_logger.info.assert_not_called()


def test_send_email_mailjet_no_to_name(mocker, settings, email_params):
    settings.EMAIL_BACKEND = "mailjet"
    mock_response = mocker.MagicMock(
        status_code=200, json=mocker.MagicMock(return_value={"Messages": []})
    )
    mock_client = mocker.patch("grants.utils.email.Client")
    mock_client.return_value.send.create.return_value = mock_response
    mocker.patch("grants.utils.email.config", side_effect=lambda x: "dummy_value")
    mock_logger = mocker.patch("grants.utils.email.logger")

    email_params["to_name"] = None
    result = send_email(**email_params)

    assert result is True
    called_data = mock_client.return_value.send.create.call_args[1]["data"]
    assert called_data["Messages"][0]["To"][0]["Name"] == ""
    mock_logger.info.assert_called_once()
    mock_logger.error.assert_not_called()


def test_send_email_mailjet_invalid_subject(mocker, settings):
    settings.EMAIL_BACKEND = "mailjet"
    mock_client = mocker.patch("grants.utils.email.Client")
    mocker.patch("grants.utils.email.config", side_effect=lambda x: "dummy_value")
    mock_logger = mocker.patch("grants.utils.email.logger")

    result = send_email(
        subject="",
        text_content="Test Text",
        html_content="<p>Test HTML</p>",
        from_email="sender@example.com",
        from_name="Sender",
        to_email="recipient@example.com",
    )

    assert result is False
    mock_client.assert_not_called()
    mock_logger.info.assert_not_called()
    mock_logger.error.assert_not_called()
