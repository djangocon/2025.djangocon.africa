from libs.mailjet import MailClient
from core.settings_base import MAILJET


def message():
    sender_email = MAILJET["SENDER_EMAIL"]
    subject = "A message from DjangoCon Africa"
    recipient_email = MAILJET["RECIPIENT_EMAIL"]
    data = {
        "Messages": [
            {
                "From": {"Email": sender_email, "Name": "DjangoCon Africa 2025"},
                "To": [{"Email": recipient_email, "Name": ""}],
                "Subject": subject,
                "TextPart": "Hi, This is DjangoCon Africa! May the  force be with you!",
                "HtmlPart": '<h3>Hi, welcome to <a href="https://www.2025.djangocon.africa/">DjangoCon Africa</a>!<br />May the delivery force be with you!',
            }
        ]
    }
    return data


def test_success_email_sending():
    data = message()
    mailjet_test = MailClient()
    result = mailjet_test.send_message(data)
    assert result.status_code == 200
