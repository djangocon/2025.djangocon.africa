from dataclasses import dataclass, field
from typing import List 
# from django.urls import reverse

@dataclass
class HeaderLink:
    label: str
    href: str = ""
    children: List["HeaderLink"] =field(default_factory=list)


header_menu_items = [
  HeaderLink(
      label="Home",
      href="/"
  ),
  HeaderLink(
      label="About",
      children = [
        #   HeaderLink("Team", href=reverse("page_team")),
          
      ]
  ),
]