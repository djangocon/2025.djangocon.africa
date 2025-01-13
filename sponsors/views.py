from django.views.generic import TemplateView
from sponsors.models import Sponsor



class SponsorsDetailView(TemplateView):
    template_name = "sponsors/sponsors.html"
    model = Sponsor

