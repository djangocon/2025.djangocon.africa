from django.test  import TestCase, Client
from custom_auth.models import User
from django.core import mail


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            first_name="Alice",
            last_name="Nolastname",
            email="alice@wonderland.com",
            password="nfpt30x49q2obt9"
        )

    def test_register_new_member(self):
        response = self.client.post("/accounts/register/",
                               dict(email="rabbit.white@wonderland.com",
                                    last_name="Rabbit", first_name="White",
                                    password1="FNEYghfr",
                                    password2="FNEYghfr"),
                               format="text/html")
        self.assertRedirects(response, "/accounts/login/", status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)
        self.assertEqual(len(mail.outbox), 1)

    def test_get_register_page(self):
        response = self.client.get("/accounts/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_valid_template_for_forgotten_password(self):
        response = self.client.get("/accounts/password_reset/")
        self.assertTemplateUsed(response, "registration/password_reset_form.html")

    def test_valid_email_sending_for_forgotten_password(self):
        u = User.objects.get(email="alice@wonderland.com")
        response = self.client.post("/accounts/password_reset/",
                                    dict(email=u.email),
                                   format="text/html")
        self.assertRedirects(response, "/accounts/password_reset/done/",
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)
        assert mail.outbox[0].to == [u.email]
        self.assertEqual(len(mail.outbox), 1)


    def test_valid_url_to_reset_password(self):
        u = User.objects.get(email="alice@wonderland.com")
        response_0 = self.client.post("/accounts/password_reset/",
                                    dict(email=u.email),
                                   format="text/html")
        email_lines = mail.outbox[0].body.splitlines()
        reset_password_url = email_lines[2].replace(" ", "")
        response = self.client.post(
            reset_password_url,
            dict(password1="3OPHWv9S3ZI", password2="3OPHWv9S3ZI",email=u.email),
            format="text.html",
        )
        self.assertEqual(response.status_code, 200)
