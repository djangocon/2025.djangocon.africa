from django.shortcuts import render
from website.models import OpportunityGrants
from django.conf import settings
from datetime import datetime

from website.constants import SCHEDULES


def page_home(request):

    return render(
        request, "page_home.html", {"is_white_header": False, "schedule": SCHEDULES}
    )


def page_coc(request):
    return render(request, "page_coc.html")


def page_news_detail(request, slug):
    return render(request, "page_news_detail.html")


def page_speaking(request):
    return render(request, "page_speaking.html")


def page_speaker_resources(request):
    return render(request, "page_speaker_resources.html")


def page_sponsor_us(request):
    return render(request, "page_sponsor_us.html")


def page_welcome(request):
    return render(request, "page_welcome.html")


def page_venue(request):
    return render(request, "page_venue.html")


def page_visa_info(request):
    return render(request, "page_visa_info.html")


def page_ticket(request):
    context = {"is_white_header": False, "uza_api_key": settings.UZA_PUBLIC_API_KEY}
    return render(request, "page_tickets.html", context)


def opportunity_grants(request):
    og_state = OpportunityGrants.objects.first()
    return render(
        request,
        "page_opportunity_grants.html",
        {
            "og_state": og_state,
            "og_is_before": (
                og_state.closing_date > datetime.now(og_state.closing_date.tzinfo)
                if og_state
                else None
            ),
        },
    )
