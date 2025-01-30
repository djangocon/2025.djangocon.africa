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
            HeaderLink(label=_("About the conference"), href="#"),
            HeaderLink(label=_("Venue"), href="#"),
            HeaderLink(label=_("Code of Conduct"), href="/coc"),
            HeaderLink(label=_("Organisers"), href="#"),
        ]
    ),
    HeaderLink(
        label=_("Resources"),
        children=[
            HeaderLink(label=_("Documentation"), href="#"),
            HeaderLink(label=_("Resources"), href="#"),
        ]
    ),
    HeaderLink(
        label=_("Speaking"),
        href="/speaking",
    ),
    HeaderLink(
        label=_("Sponsors"),
        children=[
            HeaderLink(label=_("Our Sponsors"), href="#"),
            HeaderLink(label=_("Become a Sponsor"), href="#"),
        ]
    ),
    HeaderLink(
        label=_("Schedule"),
        href="#",
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
