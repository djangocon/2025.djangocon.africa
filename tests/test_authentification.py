import  pytest
from django.test  import Client
from custom_auth.models import User

TEST_EMAIL = "yuki@djangocon.com"
TEST_PASSWORD = "nfpt30x49q2obt9"


@pytest.fixture
def user_sample():
    return User.create_user(TEST_EMAIL, TEST_PASSWORD)
 

@pytest.mark.django_db
def test_login_with_valid_credential(user_sample):
    client = CLient()
    response = client.post("accounts/login", dict(email=TEST_EMAIL,password=TEST_PASSWORD), content_type="application/json",)
    assert response.status_code == 200
    assert "sessionid"  in client.cookies

