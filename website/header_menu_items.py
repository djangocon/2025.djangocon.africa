from dataclasses import dataclass, field
from typing import List

from django.urls import reverse
from django.utils.translation import gettext as _

from .views import page_home


@dataclass
class HeaderLink:
    label: str
    href: str = ""
    children: List["HeaderLink"] = field(default_factory=list)


header_menu_items = [
    HeaderLink(label=_("Home"), href="/"),
    # HeaderLink(
    #     label="About",
    #     children=[
    #         #   HeaderLink("Team", href=reverse("page_team")),
    #     ],
    # ),
    HeaderLink(
       label=_("Sponsors"),
       children=[
            HeaderLink(_("Sponsor Us"), href=reverse("page_home")),
            HeaderLink(_("Our Sponsors"), href=reverse("page_home")),
            HeaderLink(_("Donate"), href=reverse("page_home")),
        ],
    ),
]

user_loggedin_link = HeaderLink(
    label='<i class="fas fa-user"></i> User',
    children=[
        # HeaderLink("Profile", href="todo"),
        # HeaderLink("Talk Submissions", href="todo"),
        HeaderLink(_("Logout"), href=reverse("logout")),
    ],
)

user_not_loggedin_link = HeaderLink(
    label='<i class="fas fa-user"></i> Login/Register', href=reverse("login")
)

