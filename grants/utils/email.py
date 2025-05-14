import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from mailjet_rest import Client
from decouple import config

logger = logging.getLogger(__name__)


def send_email(
    subject, text_content, html_content, from_email, from_name, to_email, to_name=None
):
    # Validate inputs
    if not to_email or not subject or not text_content:
        return False

    if settings.EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend":
        try:
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=f"{from_name} <{from_email}>",
                to=[to_email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            logger.info(f"Email sent to {to_email} via console backend")
            return True
        except Exception as e:
            logger.error(f"Error sending email via console backend: {e}")
            return False
    else:
        try:
            api_key = config("MAILJET_API_KEY")
            api_secret = config("MAILJET_SECRET_KEY")
            mailjet = Client(auth=(api_key, api_secret), version="v3.1")
            data = {
                "Messages": [
                    {
                        "From": {"Email": from_email, "Name": from_name},
                        "To": [{"Email": to_email, "Name": to_name or ""}],
                        "Subject": subject,
                        "TextPart": text_content,
                        "HTMLPart": html_content,
                    }
                ]
            }
            result = mailjet.send.create(data=data)
            logger.info(
                f"Mailjet response: Status={result.status_code}, Data={result.json()}"
            )
            if result.status_code == 200:
                return True
            else:
                logger.error(
                    f"Mailjet failed: Status={result.status_code}, Data={result.json()}"
                )
                return False
        except Exception as e:
            logger.error(f"Error sending email via Mailjet: {e}")
            return False
