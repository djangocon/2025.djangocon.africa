from django.shortcuts import render


def page_home(request):
    return render(request, "page_home.html")


def page_coc(request):
    return render(request, "page_coc.html", {"is_white_header": True})
