import pytest
from datetime import date, time
from schedule.models import Speaker, Room, ConferenceDay, Session


class TestSpeaker:

    @pytest.mark.django_db
    def test_speaker_creation(self):
        speaker = Speaker.objects.create(
            name="Jane Doe",
            bio="Senior developer with 10 years experience",
            company="Tech Corp",
            email="jane@techcorp.com",
            github="janedoe",
            twitter="jane_doe"
        )

        assert speaker is not None
        assert speaker.name == "Jane Doe"
        assert speaker.company == "Tech Corp"
        assert speaker.email == "jane@techcorp.com"

    @pytest.mark.django_db
    def test_speaker_str_method(self):
        speaker = Speaker.objects.create(name="John Smith")
        assert str(speaker) == "John Smith"

    @pytest.mark.django_db
    def test_speaker_social_links_property(self):
        speaker = Speaker.objects.create(
            name="Social Speaker",
            github="socialspeaker",
            twitter="social_speaker",
            linkedin="https://linkedin.com/in/social-speaker",
            mastodon="@user@mastodon.social",
            bluesky="socialuser",
            email="social@example.com"
        )

        links = speaker.social_links
        assert len(links) == 6  # GitHub, Twitter, LinkedIn, Mastodon, BlueSky, Email
        
        github_link = next((link for link in links if link['name'] == 'GitHub'), None)
        assert github_link is not None
        assert github_link['url'] == 'https://github.com/socialspeaker'
        assert github_link['icon'] == 'github'

        email_link = next((link for link in links if link['name'] == 'Email'), None)
        assert email_link is not None
        assert email_link['url'] == 'mailto:social@example.com'

        mastodon_link = next((link for link in links if link['name'] == 'Mastodon'), None)
        assert mastodon_link is not None
        assert mastodon_link['url'] == 'https://mastodon.social/@user'
        assert mastodon_link['icon'] == 'mastodon'

        bluesky_link = next((link for link in links if link['name'] == 'BlueSky'), None)
        assert bluesky_link is not None
        assert bluesky_link['url'] == 'https://bsky.app/profile/socialuser'
        assert bluesky_link['icon'] == 'bluesky'


class TestRoom:

    @pytest.mark.django_db
    def test_room_creation(self):
        room = Room.objects.create(name="Main Auditorium")

        assert room is not None
        assert room.name == "Main Auditorium"

    @pytest.mark.django_db
    def test_room_str_method(self):
        room = Room.objects.create(name="Conference Room A")
        assert str(room) == "Conference Room A"


class TestConferenceDay:

    @pytest.mark.django_db
    def test_conference_day_creation(self):
        conf_day = ConferenceDay.objects.create(
            name="Mon 12 Aug",
            date=date(2025, 8, 12),
            order=1
        )

        assert conf_day is not None
        assert conf_day.name == "Mon 12 Aug"
        assert conf_day.date == date(2025, 8, 12)
        assert conf_day.order == 1
        assert conf_day.is_active is True  # Default value

    @pytest.mark.django_db
    def test_conference_day_str_method(self):
        conf_day = ConferenceDay.objects.create(
            name="Tuesday",
            date=date(2025, 8, 13)
        )
        assert str(conf_day) == "Tuesday"

    @pytest.mark.django_db
    def test_conference_day_ordering(self):
        day1 = ConferenceDay.objects.create(
            name="Day 1", date=date(2025, 8, 12), order=2
        )
        day2 = ConferenceDay.objects.create(
            name="Day 2", date=date(2025, 8, 13), order=1
        )

        ordered_days = list(ConferenceDay.objects.all())
        assert ordered_days[0] == day2  # order=1 comes first
        assert ordered_days[1] == day1  # order=2 comes second


class TestSession:

    @pytest.fixture
    def sample_data(self):
        speaker = Speaker.objects.create(name="Test Speaker")
        room = Room.objects.create(name="Test Room")
        conf_day = ConferenceDay.objects.create(
            name="Test Day", date=date(2025, 8, 12)
        )
        return {
            'speaker': speaker,
            'room': room,
            'conference_day': conf_day
        }

    @pytest.mark.django_db
    def test_session_creation(self, sample_data):
        session = Session.objects.create(
            title="Test Session",
            description="A test session",
            session_type="talk",
            speaker=sample_data['speaker'],
            room=sample_data['room'],
            conference_day=sample_data['conference_day'],
            start_time=time(10, 0),
            end_time=time(11, 0)
        )

        assert session is not None
        assert session.title == "Test Session"
        assert session.session_type == "talk"
        assert session.speaker == sample_data['speaker']
        assert session.room == sample_data['room']
        assert session.start_time == time(10, 0)
        assert session.end_time == time(11, 0)
        assert session.is_break is False  # Default value

    @pytest.mark.django_db
    def test_session_type_display(self, sample_data):
        session = Session.objects.create(
            title="Keynote Session",
            session_type="keynote",
            room=sample_data['room'],
            conference_day=sample_data['conference_day'],
            start_time=time(10, 0),
            end_time=time(11, 0)
        )

        assert session.session_type_display == "Keynote"

    @pytest.mark.django_db
    def test_session_slug_auto_generation(self, sample_data):
        session = Session.objects.create(
            title="Auto Slug Generation Test",
            room=sample_data['room'],
            conference_day=sample_data['conference_day'],
            start_time=time(10, 0),
            end_time=time(11, 0)
        )

        assert session.slug == "auto-slug-generation-test"

    @pytest.mark.django_db
    def test_session_slug_uniqueness(self, sample_data):
        # Create first session
        session1 = Session.objects.create(
            title="Duplicate Title",
            room=sample_data['room'],
            conference_day=sample_data['conference_day'],
            start_time=time(10, 0),
            end_time=time(11, 0)
        )

        # Create second session with same title
        session2 = Session.objects.create(
            title="Duplicate Title",
            room=sample_data['room'],
            conference_day=sample_data['conference_day'],
            start_time=time(14, 0),
            end_time=time(15, 0)
        )

        assert session1.slug == "duplicate-title"
        assert session2.slug == "duplicate-title-1"

    @pytest.mark.django_db
    def test_session_time_range_property(self, sample_data):
        session = Session.objects.create(
            title="Time Range Test",
            room=sample_data['room'],
            conference_day=sample_data['conference_day'],
            start_time=time(14, 30),
            end_time=time(15, 45)
        )

        assert session.time_range == "02:30pm - 03:45pm"

    @pytest.mark.django_db
    def test_session_str_method(self, sample_data):
        session = Session.objects.create(
            title="String Test Session",
            room=sample_data['room'],
            conference_day=sample_data['conference_day'],
            start_time=time(15, 30),
            end_time=time(16, 30)
        )

        expected = "String Test Session - Test Day 15:30:00"
        assert str(session) == expected

    @pytest.mark.django_db
    def test_session_break_session(self, sample_data):
        break_session = Session.objects.create(
            title="Lunch Break",
            room=sample_data['room'],
            conference_day=sample_data['conference_day'],
            start_time=time(12, 0),
            end_time=time(13, 0),
            is_break=True
        )

        assert break_session.is_break is True 