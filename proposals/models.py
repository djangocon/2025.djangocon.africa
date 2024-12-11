from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ProposalType(models.Model):
    "Eg: short talk, long talk, poster, workshop..."
    name = models.CharField(max_length=128)
    description = models.TextField()
    max_duration_minutes = models.SmallIntegerField(null=True, blank=True)
    max_duration_hours = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Track(models.Model):
    """Examples: Community, Education, Frontend, Backend, Fullstack, Deployment, Other"""

    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"


class Proposal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proposal_type = models.ForeignKey(ProposalType, on_delete=models.PROTECT)
    track = models.ForeignKey(Track, on_delete=models.PROTECT)

    title = models.CharField(max_length=256)
    description = models.TextField()
    private_notes = models.TextField(null=True, blank=True)

    additional_speaker_emails = models.CharField(max_length=256, null=True, blank=True)

    LEVEL_BEGINNER = "b"
    LEVEL_INTERMEDIATE = "i"
    LEVEL_ADVANCED = "a"
    LEVEL_NON_TECHNICAL = "n"
    AUDIENCE_LEVEL_CHOICES = [
        (LEVEL_BEGINNER, "Beginner - just starting"),
        (LEVEL_INTERMEDIATE, "Intermediate"),
        (LEVEL_ADVANCED, "Advanced"),
        (LEVEL_NON_TECHNICAL, "Non technical talk"),
    ]
    audience_level = models.CharField(choices=AUDIENCE_LEVEL_CHOICES)

    accessibility_requests = models.TextField(blank=True, null=True)

    STATUS_SUBMITTED = "submitted"
    STATUS_REJECTED = "rejected"
    STATUS_ACCEPTED = "accepted"
    STATUS_SHORTLIST = "shortlisted"
    STATUS_BACKUP = "backup"

    STATUS_CHOICES = [
        (STATUS_SUBMITTED, "Submitted"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_SHORTLIST, "Shortlisted"),
        (STATUS_BACKUP, "Backup"),
    ]
    status = models.CharField(choices=STATUS_CHOICES, default=STATUS_SUBMITTED)

    def __str__(self):
        return f"{self.title}"


class ReviewAspect(models.Model):
    name = models.CharField()
    # slug = TODO

    DATA_TYPE_SCORE = "score"
    DATA_TYPE_BOOLEAN = "true/false"

    DATA_TYPE_CHOICES = [
        (DATA_TYPE_BOOLEAN, DATA_TYPE_BOOLEAN),
        (DATA_TYPE_SCORE, DATA_TYPE_SCORE),
    ]
    data_type = models.CharField(choices=DATA_TYPE_CHOICES)

    # if we are using a SCORE datatype then these are used
    minimum_score = models.SmallIntegerField(default=0)
    maximum_score = models.SmallIntegerField(default=4)

    help_text = (
        models.TextField()
    )  # use this to describe the aspect. Eg 0=terrible, 5=awesome


class Review(models.Model):
    reviewer_user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField()

    hard_no = models.BooleanField(default=False)
    favourite = models.BooleanField(default=False)


class ReviewAspectScore(models.Model):
    aspect = models.ForeignKey(ReviewAspect, on_delete=models.PROTECT)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    score = models.SmallIntegerField(null=True, blank=True)
    bool = models.BooleanField(null=True, blank=True)
