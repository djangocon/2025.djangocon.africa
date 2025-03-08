from django import template

from news.models import NewsPage

register = template.Library()

@register.simple_tag
def latest_news(count: int):
    return NewsPage.objects.live().order_by("-first_published_at")[:count]


@register.inclusion_tag("news/mini_news_index_page.html")
def mini_latest_news():
    pass


