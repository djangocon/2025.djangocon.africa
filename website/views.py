from django.shortcuts import render
from website.models import OpportunityGrants

from datetime import datetime


def page_home(request):
    schedule = [
        [
            [('Jan 3rd', 'Announce Conference', True)],
            [('Jul 7th', 'Conference Schedule is announced', False)],
        ],
        [
            [('Feb 1st', 'Call For Proposals open', True),
             ('Feb 14th', 'Opportunity Grant opens', False)],
            [('Aug 8th', 'Django Girls starts', False),
             ('Aug 9th', 'Django Girls ends', False)],
        ],
        [
            [('Mar 1st', 'Ticket sales open', False),
             ('Mar 31st', 'Call For Proposals close', False)],
            [('Aug 11th', 'Conference starts', False),
             ('Aug 15th', 'Conference ends', False)],
        ],
        [
            [('Apr 1st', 'Opportunity Grants notifications', False),
             ('Apr 1st', 'Call For Proposals notifications', False)],
            [('Aug 13th', 'UbuCon starts', False),
             ('Aug 15th', 'UbuCon ends', False)],
        ],
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
    return render(request, "page_sponsor_us.html", {"is_white_header": True})


def opportunity_grants(request):
    og_state = OpportunityGrants.objects.first()
    return render(
        request,
        "page_opportunity_grants.html",
        {
            "og_state": og_state,
            "og_is_before": og_state.closing_date > datetime.now(og_state.closing_date.tzinfo) if og_state else None,
        }
    )
