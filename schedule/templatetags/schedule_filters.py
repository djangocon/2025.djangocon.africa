from django import template

register = template.Library()


@register.filter
def format_time(time_obj):
    """Format a time object to display format (e.g., '10:30am')"""
    if not time_obj:
        return ""
    return time_obj.strftime('%I:%M%p').lower().lstrip('0')


@register.inclusion_tag('schedule/components/session_card.html')
def session_card(session):
    """Render a session card component"""
    return {
        'session': session,
    }


@register.inclusion_tag("schedule/components/speaker/single_speaker.html")
def single_speaker(speaker):
    """Render single speaker info"""
    return {
        "speaker": speaker,
    }


@register.inclusion_tag("schedule/components/speaker/multiple_speakers.html")
def multiple_speaker(speakers):
    """Render multiple speaker info"""
    return {
        "speakers": speakers,
    }


@register.inclusion_tag("schedule/components/social_links.html")
def social_links(socials):
    """Render speaker social links"""
    return {
        "social_links": socials,
    }


@register.simple_tag
def get_session_emoji(session):
    """Return emoji based on the session"""
    emojis = {
        "is_break": "🥗",
        "is_check_in": "🛎️",
        "is_opening": "👋",
        "is_closing": "🙏",
        "lighting": "⚡️",
    }
    if session.is_break:
        return emojis["is_break"]
    elif session.is_check_in:
        return emojis["is_check_in"]
    elif session.is_opening:
        return emojis["is_opening"]
    elif session.is_closing:
        return emojis["is_closing"]
    elif session.session_type == "lighting":
        return emojis["lighting"]
    else:
        return ""


@register.simple_tag
def get_all_speakers(session):
    """Return all speakers for the session"""
    return session.speaker.all()


@register.simple_tag
def is_lighting_talk(session):
    """Check if the session is a lighting talk"""
    return session.session_type.lower() == "lighting"

@register.simple_tag
def join_speakers_names(speakers):
    """Return human-readable speakers names"""
    if not speakers:
        return ""

    if speakers.count() == 1:
        return speakers[0].name
    elif speakers.count() == 2:
        return " and ".join([speaker.name for speaker in speakers])

    return ", ".join([speaker.name for speaker in speakers[:speakers.count() - 1]]) + " and " + speakers.last().name
