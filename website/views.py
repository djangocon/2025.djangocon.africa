from django.shortcuts import render


def page_home(request):
    return render(request, "page_home.html")
