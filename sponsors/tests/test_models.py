import pytest

from typing import List, Tuple
from sponsors.models import Sponsor, SponsorshipPackage


def create_package(name: str, amount: float) -> SponsorshipPackage:
    """Create a sponsor"""
    package = SponsorshipPackage.objects.create(
        name=name,
        amount=amount
    )
    return package


def create_sponsor(name: str, packages: List[Tuple[str, float]]) -> Sponsor:
    """Create a sponsor with the given name and packages."""
    sponsor = Sponsor.objects.create(name=name)
    for name, amount in packages:
        package = create_package(name, amount)
        sponsor.packages.add(package)
    sponsor.save()
    return sponsor



class TestSponsorshipModels:

    @pytest.mark.django_db
    def test_sponsorship_package_creation(self):
        package = create_package(u"Gold", 1000)

        assert package is not None
        assert package.name == u"Gold"
        assert package.amount == 1000

    @pytest.mark.django_db
    def test_sponsorship_with_single_package(self):
        """Create sponsor with multiple sponsorship packages."""
        sponsor = create_sponsor(u"Django", [
            (u"Gold", 1000)
        ])

        assert sponsor is not None
        assert sponsor.name == u"Django"
        assert sponsor.packages.count() == 1

        package = sponsor.packages.first()

        assert package is not None
        assert package.name == u"Gold"
        assert package.amount == 1000



