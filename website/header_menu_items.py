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
    HeaderLink(
        label="About",
        children=[
            #   HeaderLink("About DjangoCon Africa", href=reverse("page_about")),
            #   HeaderLink("Tickets", href=reverse("page_tickets")),
            #   HeaderLink("FAQ", href=reverse("page_faq")),
            HeaderLink("Code of Conduct", href=reverse("page_code_of_conduct")),
            # Public HEalth
            # Opportunity Grants
            # Visa Support
            # Organisers
        ],
    ),
]

user_loggedin_link = HeaderLink(
    label='<i class="fas fa-user"></i> User',
    children=[
        # HeaderLink("Profile", href="todo"),
        HeaderLink("Talk Proposals", href=reverse("my_proposals")),
        HeaderLink("Logout", href=reverse("logout")),
    ],
)

user_not_loggedin_link = HeaderLink(
    label='<i class="fas fa-user"></i> Login/Register', href=reverse("login")
)
