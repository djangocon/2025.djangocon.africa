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


@register.simple_tag
def get_session_emoji(session):
    """Return emoji based on the session"""
    emojis = {
        "is_break": "🥗",
        "is_check_in": "🛎️",
        "is_opening": "👋" ,
        "is_closing": "🙏",
    }
    if session.is_break:
        return emojis["is_break"]
    elif session.is_check_in:
        return emojis["is_check_in"]
    elif session.is_opening:
        return emojis["is_opening"]
    elif session.is_closing:
        return emojis["is_closing"]
    else:
        return ""
