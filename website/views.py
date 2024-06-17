from django.shortcuts import render


def index(request):
    return render(request, "website/index.html", {"title": "Home"})


def about(request):
    return render(request, "website/about.html", {"title": "About"})


def coc(request):
    return render(request, "website/coc.html", {"title": "Code of Conduct"})


def information(request):
    return render(request, "website/information.html", {"title": "Information for Travellers"})


def team(request):
    return render(request, "website/team.html", {"title": "Team"})


def talks(request):
    return render(request, "website/talks.html", {"title": "Talks"})


def contact(request):
    return render(request, "website/contact.html", {"title": "Contact"})


def grants(request):
    return render(request, "website/grants.html", {"title": "Opportunity Grants"})


def venue(request):
    return render(request, "website/venue.html", {"title": "Venue"})


def cfp(request):
    return render(request, "website/cfp.html", {"title": "Call for Proposals"})


def schedule(request):
    return render(request, "website/schedule.html", {"title": "Schedule"})


def sponsor(request):
    return render(request, "website/sponsor.html", {"title": "Sponsor Us"})


def sponsors(request):
    return render(request, "website/sponsors.html", {"title": "Our Sponsor"})
