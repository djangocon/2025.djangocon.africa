from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test

from . import models
from . import forms


@login_required
def my_proposals(request):
    """show a list of talk proposals for the current logged-in user"""
    proposals = models.Proposal.objects.filter(user=request.user)

    context = {"proposals": proposals}

    return render(request, "proposals/my_proposals.html", context)


@login_required
def action_delete_my_proposal(request, proposal_id):

    proposal = get_object_or_404(models.Proposal, pk=proposal_id)
    if proposal.user != request.user:
        raise Http404("Proposal does not exist")
    proposal.delete()

    proposals = models.Proposal.objects.filter(user=request.user)

    context = {"proposals": proposals}
    return render(request, "proposals/my_proposals.html#table_body", context)


@login_required
def create_proposal(request):
    if request.method == "POST":
        form = forms.ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.user = request.user
            proposal.save()
            return HttpResponseRedirect(reverse("my_proposals"))
    else:
        form = forms.ProposalForm()
    context = {"form": form}
    return render(request, "proposals/create_proposal.html", context)


@login_required
def edit_my_proposal(request, proposal_id):
    proposal = get_object_or_404(models.Proposal, pk=proposal_id)
    if proposal.user != request.user:
        raise Http404("Proposal does not exist")

    if request.method == "POST":
        form = forms.ProposalForm(request.POST, instance=proposal)
        if form.is_valid():
            proposal = form.save()
            return HttpResponseRedirect(reverse("my_proposals"))
    else:
        form = forms.ProposalForm(instance=proposal)

    context = {"form": form}
    return render(request, "proposals/edit_proposal.html", context)


@user_passes_test(lambda user: user.is_reviewer)
def reviewer_dashboard(request):

    proposals = models.Proposal.objects.all()  # TODO: filter appropriately
    context = {"proposals": proposals}
    return render(request, "proposals/reviewer_dashboard.html", context)


from django import forms


def aspect_to_form_field(aspect: models.ReviewAspect):
    if aspect.data_type == aspect.DATA_TYPE_BOOLEAN:
        return forms.NullBooleanField(
            widget=forms.Select(
                choices=[
                    ("", "Unknown"),
                    (True, "Yes"),
                    (False, "No"),
                ]
            ),
            help_text=aspect.help_text,
        )
    if aspect.data_type == aspect.DATA_TYPE_SCORE:
        return forms.IntegerField(
            max_value=aspect.maximum_score,
            min_value=aspect.minimum_score,
            help_text=aspect.help_text,
        )


def create_review_form_class():

    properties = {
        aspect.name: aspect_to_form_field(aspect)
        for aspect in models.ReviewAspect.objects.all()
    }

    class ReviewFormMeta(forms.models.ModelFormMetaclass):
        model = models.Review

        fields = ["notes", "hard_no", "favourite"]
        help_texts = {
            "hard_no": "Tick this box if you are strongly against accepting this talk",
            "favourite": "Tick this box if you are really keen to see this talk",
        }

    properties["Meta"] = ReviewFormMeta

    ReviewFrom = type("ReviewFrom", (forms.ModelForm,), properties)

    return ReviewFrom


@user_passes_test(lambda user: user.is_reviewer)
def add_edit_review(request, proposal_id):
    # TODO: Cant reviwe own proposal
    proposal = get_object_or_404(models.Proposal, pk=proposal_id)
    ReviewFrom = create_review_form_class()

    form = ReviewFrom()
    context = {"form": form, "proposal": proposal}

    return render(request, "proposals/add_edit_review.html", context=context)
