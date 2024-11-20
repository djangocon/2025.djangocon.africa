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
                               dict(email=u.email,password=u.password), content_type="application/json",)
        assert response.status_code == 200
        assert u.is_authenticated == True

