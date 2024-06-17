from django.urls import reverse


def test_index_page_path(client):
    response = client.get("/")
    assert response.status_code == 200


def test_index_page_view(client):
    response = client.get(reverse("website:home"))
    assert response.status_code == 200


def test_abouth_page_path(client):
    response = client.get("/about/")
    assert response.status_code == 200


def test_about_page_view(client):
    response = client.get(reverse("website:about"))
    assert response.status_code == 200


def test_coc_page_path(client):
    response = client.get("/coc/")
    assert response.status_code == 200


def test_coc_page_view(client):
    response = client.get(reverse("website:coc"))
    assert response.status_code == 200


def test_information_page_path(client):
    response = client.get("/information/")
    assert response.status_code == 200


def test_information_page_view(client):
    response = client.get(reverse("website:information"))
    assert response.status_code == 200


def test_team_page_path(client):
    response = client.get("/team/")
    assert response.status_code == 200


def test_team_page_view(client):
    response = client.get(reverse("website:team"))
    assert response.status_code == 200


def test_talks_page_path(client):
    response = client.get("/talks/")
    assert response.status_code == 200


def test_talks_page_view(client):
    response = client.get(reverse("website:talks"))
    assert response.status_code == 200


def test_contact_page_path(client):
    response = client.get("/contact/")
    assert response.status_code == 200


def test_contact_page_view(client):
    response = client.get(reverse("website:contact"))
    assert response.status_code == 200


def test_grants_page_path(client):
    response = client.get("/grants/")
    assert response.status_code == 200


def test_grants_page_view(client):
    response = client.get(reverse("website:grants"))
    assert response.status_code == 200


def test_venue_page_path(client):
    response = client.get("/venue/")
    assert response.status_code == 200


def test_venue_page_view(client):
    response = client.get(reverse("website:venue"))
    assert response.status_code == 200


def test_cfp_page_path(client):
    response = client.get("/cfp/")
    assert response.status_code == 200


def test_cfp_page_view(client):
    response = client.get(reverse("website:cfp"))
    assert response.status_code == 200


def test_schedule_page_path(client):
    response = client.get("/schedule/")
    assert response.status_code == 200


def test_schedule_page_view(client):
    response = client.get(reverse("website:schedule"))
    assert response.status_code == 200


def test_sponsor_page_path(client):
    response = client.get("/sponsor/")
    assert response.status_code == 200


def test_sponsor_page_view(client):
    response = client.get(reverse("website:sponsor"))
    assert response.status_code == 200


def test_sponsors_page_path(client):
    response = client.get("/sponsors/")
    assert response.status_code == 200


def test_sponsors_page_view(client):
    response = client.get(reverse("website:sponsors"))
    assert response.status_code == 200
