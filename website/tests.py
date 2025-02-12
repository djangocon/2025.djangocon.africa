import pytest
from django.core.exceptions import ValidationError

from django.utils import timezone

from website.models import OpportunityGrants


class TestOpportunityGrants:

    @pytest.mark.django_db
    def test_opportunity_grants_creation(self):
        closing_date = timezone.now() + timezone.timedelta(days=1)
        og = OpportunityGrants.objects.create(
            link="https://example.com",
            is_open=True,
            closing_date=closing_date
        )

        assert og is not None
        assert og.link == "https://example.com"
        assert og.is_open
        assert og.closing_date == closing_date


    @pytest.mark.django_db
    def test_multiple_opportunities_grants_link_creation(self):
        """make sure only a single opportunities grants is opened"""
        with pytest.raises(ValidationError) as exc_info:
            closing_date = timezone.now() + timezone.timedelta(days=1)
            OpportunityGrants.objects.create(link="https://example.com", is_open=True, closing_date=closing_date)
            OpportunityGrants.objects.create(link="https://example.com", is_open=False, closing_date=closing_date)

        assert isinstance(exc_info.value, ValidationError)

