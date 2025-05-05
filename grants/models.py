# grants/models.py
from django.db import models
from django.utils import timezone

class GrantApplication(models.Model):
    GRANT_TYPES = (
        ('TRAVEL', 'Travel'),
        ('TICKET', 'Conference Ticket'),
        ('FULL', 'Full (Travel + Ticket)'),
        ('SPEAKER', 'Speaker'),
    )

    TICKET_CHOICES = (
        ('YES', 'Yes'),
        ('NO', 'No'),
    )

    timestamp = models.DateTimeField()
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    profession = models.CharField(max_length=200)
    country_of_origin = models.CharField(max_length=100)
    city_of_travel = models.CharField(max_length=100)
    ticket_only = models.CharField(max_length=50, choices=TICKET_CHOICES)
    grant_type = models.CharField(max_length=100, choices=GRANT_TYPES)
    budget_details = models.TextField(blank=True, default='')  # Allow blank
    status = models.CharField(
        max_length=20,
        choices=(('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')),
        default='PENDING'
    )

    def __str__(self):
        return f"{self.full_name} - {self.email}"

    class Meta:
        ordering = ['-timestamp']

class VerificationCode(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() <= self.expires_at

    def __str__(self):
        return f"{self.email} - {self.code}"