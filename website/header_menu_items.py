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


def get_user_loggedin_link(request):
    if not request.user.is_authenticated:
        return
    children = []
    if request.user.is_reviewer:
        children.append(HeaderLink("Reviews", href=reverse("reviewer_dashboard")))
    children.extend(
        [
            HeaderLink("Talk Proposals", href=reverse("my_proposals")),
            HeaderLink("Logout", href=reverse("logout")),
        ]
    )

    return HeaderLink(
        label=f'<i class="fas fa-user"></i> {request.user}', children=children
    )


user_not_loggedin_link = HeaderLink(
    label='<i class="fas fa-user"></i> Login/Register', href=reverse("login")
)
