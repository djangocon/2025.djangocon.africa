from django.test  import TestCase, Client
from custom_auth.models import User

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            first_name="Alice",
            last_name="Nolastname",
            email="alice@wonderland.com",
            password="nfpt30x49q2obt9"
        )

    def test_login_with_valid_credential(self):
        client = Client()
        u = User.objects.get(email="alice@wonderland.com")
        response = client.post("/accounts/login/",
                               dict(email=u.email,password=u.password),
                               content_type="application/json")
        assert response.status_code == 200
        assert u.is_authenticated == True

    def test_register_new_member(self):
        client = Client()
        response = client.post("/accounts/register/",
                               dict(email="rabbit.white@wonderland.com",
                                    last_name="Rabbit", first_name="White",
                                    password1="FNEYghfr",
                                    password2="FNEYghfr"),
                               format="text/html")
        self.assertRedirects(response, "/accounts/login/", status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)
