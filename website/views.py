from django.shortcuts import render


def page_home(request):
    return render(request, "page_home.html")


def page_code_of_conduct(request):
    return render(request, "page_code_of_conduct.html")
