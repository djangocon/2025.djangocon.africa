from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import get_template


def send_registration_email(email, username):
    template_email = get_template('registration/emails/registration_email.html')
    d = { 'username': username }
    subject, from_email, to = 'welcome', 'hello@djangoconafrica.com', email
    html_content = template_email.render(d)
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

