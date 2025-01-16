from django.conf import settings
from django.utils.translation import get_language


def language_context(request):
    current_language = get_language()
    languages_dict = dict(settings.LANGUAGES)
    return {
        'current_language': current_language,
        'current_language_name': languages_dict.get(current_language, 'English'),
    }
