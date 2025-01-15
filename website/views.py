from django.shortcuts import render


def page_home(request):
    return render(request, "page_home.html")


def page_coc(request):
    return render(request, "page_coc.html", {"is_white_header": True})


def page_news_detail(request, slug):
    return render(request, "page_news_detail.html", {"is_white_header": True})
