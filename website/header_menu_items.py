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
    HeaderLink(
        label=_("Conference"),
        children=[
            HeaderLink(label=_("About the conference"), href="/about"),
            HeaderLink(label=_("Venue"), href="/venue"),
            HeaderLink(label=_("Code of Conduct"), href="/coc"),
            HeaderLink(label=_("Organisers"), href="/organisers"),
        ]
    ),
    HeaderLink(
        label=_("Resources"),
        children=[
            HeaderLink(label=_("Documentation"), href="/docs"),
            HeaderLink(label=_("Resources"), href="/resources"),
        ]
    ),
    HeaderLink(
        label=_("Speaking"),
        href="/speaking",
    ),
    HeaderLink(
        label=_("Sponsors"),
        children=[
            HeaderLink(label=_("Our Sponsors"), href=reverse("sponsors")),
            HeaderLink(label=_("Become a Sponsor"), href="/become-sponsor"),
        ]
    ),
    HeaderLink(
        label=_("Schedule"),
        href="/schedule",
    ),
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
