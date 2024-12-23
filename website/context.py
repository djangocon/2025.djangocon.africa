from django.conf import settings
from .header_menu_items import (
    header_menu_items,
    user_loggedin_link,
    user_not_loggedin_link,
)


def context(request):
    return {
        "header_menu_items": header_menu_items,
        "user_loggedin_link": user_loggedin_link,
        "user_not_loggedin_link": user_not_loggedin_link,
        "FEATURE_FLAGS": settings.FEATURE_FLAGS,
    }
