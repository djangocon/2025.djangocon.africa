from django import template

from sponsors.models import Sponsor, SponsorshipPackage

register = template.Library()



@register.simple_tag
def sponsors():
    return {
        "sponsors": Sponsor.objects.all().order_by('packages', 'order', 'id'),
    }


@register.inclusion_tag("sponsors/mini_sponsors_block.html")
def mini_sponsors():
    pass


@register.simple_tag
def sponsor_by_pkg_name(*args):
    sponsor_list = Sponsor.objects.all().order_by('packages__name', 'order', 'id').distinct("packages__name")
    return sponsor_list.filter(packages__name__in=args)


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
