from django.db import models
from django.utils.translation import gettext_lazy as _


class Speaker(models.Model):
    """Model for conference speakers"""
    name = models.CharField(max_length=255, help_text=_("Speaker's full name"))
    bio = models.TextField(blank=True, help_text=_("Speaker biography"))
    photo = models.ImageField(upload_to='speakers/', blank=True, null=True, help_text=_("Speaker photo"))
    company = models.CharField(max_length=255, blank=True, help_text=_("Speaker's company/organization"))

    github = models.CharField(max_length=100, blank=True, help_text=_("GitHub username"))
    twitter = models.CharField(max_length=100, blank=True, help_text=_("Twitter handle (without @)"))
    linkedin = models.URLField(blank=True, help_text=_("LinkedIn profile URL"))
    mastodon = models.CharField(max_length=200, blank=True, help_text=_("Mastodon handle (e.g., @user@instance.social)"))
    bluesky = models.CharField(max_length=100, blank=True, help_text=_("BlueSky handle (without @)"))
    email = models.EmailField(blank=True, help_text=_("Speaker email"))

    class Meta:
        verbose_name = _("Speaker")
        verbose_name_plural = _("Speakers")
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def social_links(self):
        """Return a list of social media links for the speaker"""
        links = []
        if self.github:
            links.append({
                'name': 'GitHub',
                'url': f'https://github.com/{self.github}',
                'icon': 'github'
            })
        if self.twitter:
            links.append({
                'name': 'Twitter/X',
                'url': f'https://twitter.com/{self.twitter}',
                'icon': 'twitter'
            })
        if self.linkedin:
            links.append({
                'name': 'LinkedIn',
                'url': self.linkedin,
                'icon': 'linkedin'
            })
        if self.mastodon:
            mastodon_handle = self.mastodon.lstrip('@')
            if '@' in mastodon_handle:
                username, instance = mastodon_handle.split('@', 1)
                links.append({
                    'name': 'Mastodon',
                    'url': f'https://{instance}/@{username}',
                    'icon': 'mastodon'
                })
        if self.bluesky:
            links.append({
                'name': 'BlueSky',
                'url': f'https://bsky.app/profile/{self.bluesky}',
                'icon': 'bluesky'
            })
        if self.email:
            links.append({
                'name': 'Email',
                'url': f'mailto:{self.email}',
                'icon': 'email'
            })
        return links


class Room(models.Model):
    """Model for conference rooms/venues"""
    name = models.CharField(max_length=255, help_text=_("Room name"))

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
        ordering = ['name']

    def __str__(self):
        return self.name


class ConferenceDay(models.Model):
    """Model for conference days"""
    date = models.DateField(help_text=_("Conference day date"))
    name = models.CharField(max_length=100, help_text=_("Day name (e.g., 'Mon 12 Aug')"))
    is_active = models.BooleanField(default=True, help_text=_("Whether this day is active"))
    order = models.PositiveIntegerField(default=1, help_text=_("Display order"))

    class Meta:
        verbose_name = _("Conference Day")
        verbose_name_plural = _("Conference Days")
        ordering = ['order', 'date']

    def __str__(self):
        return self.name


class Session(models.Model):
    """Model for conference sessions"""

    SESSION_TYPES = [
        ('keynote', _('Keynote')),
        ('talk', _('Talk')),
        ('workshop', _('Workshop')),
        ('panel', _('Panel')),
        ('break', _('Break')),
    ]

    title = models.CharField(max_length=255, help_text=_("Session title"))
    description = models.TextField(blank=True, help_text=_("Session description"))
    abstract = models.TextField(blank=True, help_text=_("Session abstract"))
    session_type = models.CharField(
        max_length=20,
        choices=SESSION_TYPES,
        default='talk',
        help_text=_("Type of session")
    )
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE, null=True, blank=True, help_text=_("Session speaker"))
    room = models.ForeignKey(Room, on_delete=models.CASCADE, help_text=_("Session room"))
    conference_day = models.ForeignKey(ConferenceDay, on_delete=models.CASCADE, help_text=_("Conference day"))

    start_time = models.TimeField(help_text=_("Session start time"))
    end_time = models.TimeField(help_text=_("Session end time"))

    is_break = models.BooleanField(default=False, help_text=_("Whether this is a break/lunch session"))

    # URL slug for session detail pages
    slug = models.SlugField(max_length=255, unique=True, blank=True, help_text=_("URL slug for this session"))

    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")
        ordering = ['conference_day__order', 'start_time', 'room__name']

    def __str__(self):
        return f"{self.title} - {self.conference_day.name} {self.start_time}"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Session.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def time_range(self):
        """Return formatted time range"""
        return f"{self.start_time.strftime('%I:%M%p').lower()} - {self.end_time.strftime('%I:%M%p').lower()}"

    @property
    def session_type_display(self):
        """Return display name for session type"""
        return dict(self.SESSION_TYPES).get(self.session_type, self.session_type)
