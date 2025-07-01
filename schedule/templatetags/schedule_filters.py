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