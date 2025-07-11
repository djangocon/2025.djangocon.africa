from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Organiser
from .forms import OrganiserSubmissionForm

# Create your views here.


class OrganisersListView(ListView):
    model = Organiser
    template_name = "organisers/organisers.html"
    context_object_name = "organisers"
    queryset = Organiser.objects.filter(approved=True)


class OrganiserSubmissionView(CreateView):
    model = Organiser
    form_class = OrganiserSubmissionForm
    template_name = "organisers/submit_organiser.html"
    success_url = reverse_lazy("organiser_submission_success")

    def form_valid(self, form):
        # Set approved to False by default
        form.instance.approved = False
        messages.success(
            self.request,
            "Thank you for submitting your organiser information! "
            "Your submission is pending approval and will be displayed once reviewed.",
        )
        return super().form_valid(form)


class OrganiserSubmissionSuccessView(ListView):
    """Simple success page after submission"""

    model = Organiser
    template_name = "organisers/submission_success.html"

    def get_queryset(self):
        return Organiser.objects.none()  # We don't need any data for success page
