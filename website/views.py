from django.shortcuts import render


def index(request):
    return render(request, "website/index.html", {"title": "Home"})


def about(request):
    return render(request, "website/about.html", {"title": "About"})
