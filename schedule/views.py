from django.shortcuts import render, get_object_or_404
from .models import ConferenceDay, Session


def schedule_list(request):
    """View for displaying the conference schedule"""
    conference_days = ConferenceDay.objects.filter(is_active=True).prefetch_related(
        'session_set__speaker',
        'session_set__room'
    )

    selected_day_id = request.GET.get('day')

    if selected_day_id:
        try:
            selected_day = ConferenceDay.objects.get(
                id=selected_day_id, is_active=True)
        except ConferenceDay.DoesNotExist:
            selected_day = conference_days.first() if conference_days else None
    else:
        selected_day = conference_days.first() if conference_days else None

    # Get sessions for the selected day, organized by time slots
    sessions_by_time = {}
    if selected_day:
        sessions = Session.objects.filter(conference_day=selected_day).select_related(
            'room',
        ).order_by('start_time', 'room__name')

        # Group sessions by time slot
        for session in sessions:
            time_key = f"{session.start_time}-{session.end_time}"
            if time_key not in sessions_by_time:
                sessions_by_time[time_key] = {
                    'time_range': session.time_range,
                    'sessions': []
                }
            sessions_by_time[time_key]['sessions'].append(session)

    context = {
        'conference_days': conference_days,
        'selected_day': selected_day,
        'sessions_by_time': sessions_by_time,
    }

    return render(request, "schedule/schedule_list.html", context)


def session_detail(request, slug):
    """View for displaying detailed information about a specific session"""
    session = get_object_or_404(
        Session.objects.select_related(
            'room', 'conference_day',
        ),
        slug=slug
    )

    context = {
        'session': session,
    }

    return render(request, "schedule/session_detail.html", context)
