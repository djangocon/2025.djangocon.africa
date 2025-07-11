from django.views.generic import ListView
from .models import Organiser

# Create your views here.


class OrganisersListView(ListView):
    model = Organiser
    template_name = "organisers/organisers.html"
    context_object_name = "organisers"
    queryset = Organiser.objects.all()
