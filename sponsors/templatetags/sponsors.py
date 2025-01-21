from django import template

from sponsors.models import Sponsor, SponsorshipPackage

register = template.Library()



@register.simple_tag
def sponsors():
    return {
        "sponsors": Sponsor.objects.all().order_by('packages', 'order', 'id'),
    }


@register.simple_tag
def packages():
    return {
        "packages": SponsorshipPackage.objects.all().prefetch_related("files"),
    }

@register.simple_tag
def sponsor_tagged_image(sponsor, tag):
    """return the corresponding url from the tagged image list."""
    if sponsor.files.filter(tag_name=tag).exists():
        return sponsor.files.filter(tag_name=tag).first().tagged_file.item.url
    return ''
