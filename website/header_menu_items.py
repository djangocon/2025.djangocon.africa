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
            # HeaderLink(label=_("About the conference"), href="#"),
            # HeaderLink(label=_("Venue"), href="#"),
            HeaderLink(label=_("Code of Conduct"), href="/coc"),
            # HeaderLink(label=_("Organisers"), href="#"),
        ]
    ),
    HeaderLink(
        label=_("Resources"),
        children=[
            HeaderLink(label=_("News"), href="/news"),
            HeaderLink(label=_("Opportunity Grants"), href="/opportunity_grants"),
        ]
    ),
    HeaderLink(
        label=_("Speaking"),
        children =[
            HeaderLink(label=_("Speaking at Djangocon Africa"), href="/speaking"),
            HeaderLink(label=_("Speaker Resources"), href="/speaker_resources"),
            HeaderLink(label=_("Call for Proposals"), href="https://pretalx.com/djangocon-africa-2025/cfp"),
        ]
    ),
    HeaderLink(
        label=_("Sponsors"),
        children=[
            HeaderLink(label=_("Become a Sponsor"), href="/sponsor_us"),
            HeaderLink(label=_("Our Sponsors"), href="/sponsors/"),
        ]
    ),
    # HeaderLink(label=_("Schedule"), href="#",),
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
