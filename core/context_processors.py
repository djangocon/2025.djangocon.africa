from django.conf import settings
from django.utils.translation import get_language


def language_context(request):
    current_language = get_language()
    languages_dict = dict(settings.LANGUAGES)
    return {
        'current_language': current_language,
        'current_language_name': languages_dict.get(current_language, 'English'),
        'current_language_flag': settings.LANGUAGE_FLAGS.get(current_language, '🇬🇧'),
        'supported_languages': languages_dict,
    }

def social_media_links(request):
    return {
        "social_media_links": settings.SOCIAL_MEDIA_LINKS
    }