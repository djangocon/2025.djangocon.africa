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
