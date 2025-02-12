from django.shortcuts import render
from website.models import OpportunityGrants

from datetime import datetime


def page_home(request):
    return render(request, "page_home.html")


def page_coc(request):
    return render(request, "page_coc.html", {"is_white_header": True})


def page_news_detail(request, slug):
    return render(request, "page_news_detail.html", {"is_white_header": True})


def page_speaking(request):
    return render(request, "page_speaking.html", {"is_white_header": True})


def page_speaker_resources(request):
    return render(request, "page_speaker_resources.html", {"is_white_header": True})


def page_sponsor_us(request):
    return render(request, "page_sponsor_us.html", {"is_white_header": True})


def opportunity_grants(request):
    og_state = OpportunityGrants.objects.first()
    return render(
        request,
        "page_opportunity_grants.html",
        {
            "is_white_header": True,
            "og_state": og_state,
            "og_is_before": og_state.closing_date > datetime.now(og_state.closing_date.tzinfo) if og_state else None,
        }
    )
