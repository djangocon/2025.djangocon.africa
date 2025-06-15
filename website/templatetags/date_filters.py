from django import template
from datetime import datetime
register = template.Library()


@register.filter
def format_date(date):
    """Format a date with the ordinal suffix (e.g., "Jan 1st")"""
    if not date:
        return ""
    day = date.day
    suffix = "th" if 11 <= day <= 13 else {
        1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return date.strftime(f"%b {day}{suffix}")


@register.filter
def is_past(date):
    """Check if a date is in the past."""
    if date is None:
        return False
    return date < datetime.now()
