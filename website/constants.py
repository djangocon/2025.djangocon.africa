from datetime import datetime

from django.utils.translation import gettext as _

SOCIAL_MEDIA_LINKS = {
    "Twitter/X": "https://twitter.com/djcafrica",
    "LinkedIn": "https://linkedin.com/company/djcafrica",
    "Instagram": "https://instagram.com/djcafrica",
    "Facebook": "https://facebook.com/djcafrica",
    "Masterdon": "https://fosstodon.org/@djangoconafrica/111065411415401242",
    "Bluesky": "https://bsky.app/profile/djcafrica.bsky.social",
}

SCHEDULES = [
    [(datetime(2025, 1, 23), _('Announce Conference'))],
    [
        (datetime(2025, 2, 3), _('Call For Proposals Open')),
        (datetime(2025, 2, 12), _('Call for Sponsors Open')),
        (datetime(2025, 2, 14), _('Opportunity Grant Open'))
    ],
    [
        (datetime(2025, 3, 1), _('Ticket Sales Open')),
        (datetime(2025, 3, 31), _('Opportunity Grants && Call For Proposals close')),
    ],
    [
        (datetime(2025, 4, 8), _('Talk review start')),
        (datetime(2025, 5, 31), _('Opportunity Grant && Call for Proposal Notifications'))
    ],
    [
        (datetime(2025, 8, 8), _('Django Girls starts')),
        (datetime(2025, 8, 9), _('Django Girls ends'))
    ],
    [
        (datetime(2025, 8, 11), _('Conference starts')),
        (datetime(2025, 8, 13), _('UbuCon starts'))
    ],
    [
        (datetime(2025, 8, 15), _('Conference ends')),
        (datetime(2025, 8, 15), _('UbuCon ends'))
    ]
]

