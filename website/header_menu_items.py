from dataclasses import dataclass, field
from typing import List

from django.urls import reverse
from django.utils.translation import gettext as _


@dataclass
class HeaderLink:
    label: str
    href: str = ""
    children: List["HeaderLink"] = field(default_factory=list)

header_menu_items = [
    HeaderLink(_("Home"), href="/"),
    # HeaderLink(
    #     label="About",
    #     children=[
    #         #   HeaderLink("Team", href=reverse("page_team")),
    #     ],
    # ),
]

user_loggedin_link = HeaderLink(
    label='<i class="fas fa-user"></i> User',
    children=[
        # HeaderLink("Profile", href="todo"),
        HeaderLink(_("Talk Proposals"), href=reverse("my_proposals")),
        HeaderLink(_("Logout"), href=reverse("account_logout")),
    ],
)

user_not_loggedin_link = HeaderLink(
    label=_("LogIn"),
    href=reverse("account_login")
)
