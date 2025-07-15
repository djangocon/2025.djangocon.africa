from django.conf import settings
from .header_menu_items import header_menu_items


def context(request):
    return {
        "header_menu_items": header_menu_items,
        "FEATURE_FLAGS": settings.FEATURE_FLAGS,
        "is_white_header": True,
    }
