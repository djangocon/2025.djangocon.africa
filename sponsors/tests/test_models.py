import pytest
import tempfile

from typing import List, Tuple
from sponsors.models import Sponsor, SponsorshipPackage, File, TaggedFile

from django.core.files.uploadedfile import SimpleUploadedFile

def create_package(name: str, amount: float) -> SponsorshipPackage:
    """Create a sponsor"""
    package = SponsorshipPackage.objects.create(
        name=name,
        amount=amount
    )
    return package


def create_sponsor(name: str, packages: List[Tuple[str, float]], hiring: bool = False) -> Sponsor:
    """Create a sponsor with the given name and packages."""
    sponsor = Sponsor.objects.create(name=name, hiring=hiring)
    for name, amount in packages:
        package = create_package(name, amount)
        sponsor.packages.add(package)
    sponsor.save()
    return sponsor


def create_file(name: str, desc: str) -> File:
    """Create a File with a temporary image file."""
    temp_image = tempfile.NamedTemporaryFile(suffix=".png")
    test_image = SimpleUploadedFile(
        name="test_image.png",
        content=open(temp_image.name, "rb").read(),
        content_type="image/png"
    )

    return File.objects.create(
        name=name,
        description=desc,
        item=test_image
    )


class TestSponsorshipModels:

    @pytest.mark.django_db
    def test_sponsorship_package_creation(self):
        """Create a sponsorship package."""
        package = create_package(u"Gold", 1000)

        assert package is not None
        assert package.name == u"Gold"
        assert package.amount == 1000

    @pytest.mark.django_db
    def test_sponsorship_with_single_package(self):
        """Create sponsor with single sponsorship packages."""
        sponsor = create_sponsor(u"Django", [
            (u"Gold", 1000)
        ], hiring=True)

        assert sponsor is not None
        assert sponsor.name == u"Django"
        assert sponsor.packages.count() == 1
        assert sponsor.hiring

        package = sponsor.packages.first()

        assert package is not None
        assert package.name == u"Gold"
        assert package.amount == 1000

    @pytest.mark.django_db
    def test_sponsorship_with_multiple_packages(self):
        """Creat sponsor with multiple sponsorship packages."""
        sponsor = create_sponsor(u"Django Org.", [
            (u"Gold", 1000),
            (u"Sliver", 500),
        ])

        assert sponsor is not None
        assert sponsor.name == u"Django Org."
        assert sponsor.packages.count() == 2

        packages = sponsor.packages.all()

        assert packages is not None
        assert packages.count() == 2


class TestFilesModels:

    @pytest.mark.django_db
    def test_file_creation(self):
        """Creates a file with name and description."""
        file = create_file(name="Awesome image", desc="This is a test file.")

        assert file is not None
        assert file.name == u"Awesome image"
        assert file.description == u"This is a test file."
        assert file.item

    @pytest.mark.django_db
    def test_tagged_file_creation(self):
        """Create tagged file"""
        file = create_file(name="Tagged Image", desc="This is a test file.")
        sponsor = create_sponsor(u"Awesome Sponsor", [
            (u"Gold", 1000)
        ])

        assert file is not None
        assert sponsor is not None

        tagged_file = TaggedFile.objects.create(
            tag_name="logo",
            tagged_file=file,
            sponsor=sponsor
        )

        assert tagged_file is not None
        assert tagged_file.tag_name == u"logo"
        assert tagged_file.sponsor == sponsor



