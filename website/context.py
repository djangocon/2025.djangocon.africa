from .header_menu_items import (
    header_menu_items,
    get_user_loggedin_link,
    user_not_loggedin_link,
)


def context(request):
    return {
        "header_menu_items": header_menu_items,
        "user_loggedin_link": get_user_loggedin_link(request),
        "user_not_loggedin_link": user_not_loggedin_link,
    }
