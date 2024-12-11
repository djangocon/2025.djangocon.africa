from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from proposals.models import ProposalType, Track, Proposal, ReviewAspect
import random

User = get_user_model()


class Command(BaseCommand):
    help = "Create a bunch of fake data to play with"

    def handle(self, *args, **options):
        super, _ = User.objects.get_or_create(
            is_staff=True, is_superuser=True, email="super@email.com"
        )
        super.set_password("super@email.com")
        super.save()

        p1, _ = ProposalType.objects.get_or_create(
            name="long talk",
            defaults={
                "max_duration_minutes": 40,
                "description": "A lot of talking. Really quite a lot. Best for talkative folks who like speaking. A lot",
            },
        )

        p2, _ = ProposalType.objects.get_or_create(
            name="short talk",
            defaults={
                "max_duration_minutes": 20,
                "description": "Not so much talking",
            },
        )

        p3, _ = ProposalType.objects.get_or_create(
            name="poster",
            defaults={
                "description": "No talking",
            },
        )

        proposal_types = [p1, p2, p3]

        t1, _ = Track.objects.get_or_create(name="Community")
        t2, _ = Track.objects.get_or_create(name="Ops")
        t3, _ = Track.objects.get_or_create(name="Frontend")
        t4, _ = Track.objects.get_or_create(name="Security")

        tracks = [t1, t2, t3, t4]

        ReviewAspect.objects.get_or_create(
            name="Meaningful title",
            data_type=ReviewAspect.DATA_TYPE_SCORE,
            defaults={
                "help_text": "0 = terrible\n 1 = kinda bad\n 2= ok \n 3=pretty good \n 4 =poetry"
            },
        )
        ReviewAspect.objects.get_or_create(
            name="Blatant use of LLMs",
            data_type=ReviewAspect.DATA_TYPE_BOOLEAN,
            defaults={"help_text": "Does it look like this was written by a robot?"},
        )

        def create_user_and_proposals(email, is_reviewer):
            user, _ = User.objects.get_or_create(
                email=email, defaults={"is_reviewer": is_reviewer}
            )
            user.set_password(email)
            user.save()

            for n in range(3):
                Proposal.objects.get_or_create(
                    title=f"Title for {email} proposal {n}",
                    user=user,
                    defaults={
                        "track": random.choice(tracks),
                        "proposal_type": random.choice(proposal_types),
                        "description": "The quick red fox jumps over the lazy dog" * 10,
                        "audience_level": random.choice(
                            Proposal.AUDIENCE_LEVEL_CHOICES
                        )[0],
                    },
                )

        create_user_and_proposals(email="normal@email.com", is_reviewer=False)
        create_user_and_proposals(email="reviewer1@email.com", is_reviewer=True)
        create_user_and_proposals(email="reviewer2@email.com", is_reviewer=True)
