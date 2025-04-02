from django.shortcuts import render
from website.models import OpportunityGrants
from django.conf import settings
from datetime import datetime


def page_home(request):
    schedule = [
        [(datetime(2025, 1, 3), 'Announce Conference')],
        [(datetime(2025, 2, 1), 'Call For Proposals open'),
         (datetime(2025, 2, 14), 'Opportunity Grant opens')],
        [(datetime(2025, 3, 1), 'Ticket sales open'),
         (datetime(2025, 3, 31), 'Call For Proposals close')],
        [(datetime(2025, 4, 1), 'Opportunity Grants notifications'),
         (datetime(2025, 4, 1), 'Call For Proposals notifications')],
        [(datetime(2025, 7, 7), 'Conference Schedule is announced')],
        [(datetime(2025, 8, 8), 'Django Girls starts'),
         (datetime(2025, 8, 9), 'Django Girls ends')],
        [(datetime(2025, 8, 11), 'Conference starts'),
         (datetime(2025, 8, 13), 'UbuCon starts')],
        [(datetime(2025, 8, 15), 'Conference ends'),
         (datetime(2025, 8, 15), 'UbuCon ends')]
    ]

    return render(
        request,
        "page_home.html",
        {
            "is_white_header": False,
            "schedule": schedule
        }
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
    return render(request, "page_sponsor_us.html", {"is_white_header"})


def page_ticket(request):
    context = {
        "is_white_header": False, "uza_api_key": settings.UZA_PUBLIC_API_KEY}
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
