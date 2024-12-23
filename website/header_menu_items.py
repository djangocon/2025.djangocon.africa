from dataclasses import dataclass, field
from typing import List

from django.urls import reverse


@dataclass
class HeaderLink:
    label: str
    href: str = ""
    children: List["HeaderLink"] = field(default_factory=list)

header_menu_items = [
    HeaderLink(label="Home", href="/"),
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
        HeaderLink("Talk Proposals", href=reverse("my_proposals")),
        HeaderLink("Logout", href=reverse("account_logout")),
    ],
)

user_not_loggedin_link = HeaderLink(
    label='LogIn',
    href=reverse("account_login")
)
