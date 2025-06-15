from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from datetime import date



class NewsIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    template = "news/news_index_page.html"

    def get_context(self, request):
        news = self.get_children().live().order_by('-first_published_at')
        context = super().get_context(request)
        if news:
            context['published_news'] = news
            context["latest_news"] = news[0]
        return context


class NewsPage(Page):
    intro = models.CharField(max_length=100)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
    )
    body = RichTextField(blank=True)
    date = models.DateField(
        "News Date",
        default=date.today,
    )
    caption = models.TextField(
        blank=True,
        max_length=100,
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('image'),
        FieldPanel('body'),
        FieldPanel('date'),
        FieldPanel('caption'),
    ]

    template = "news/news_page.html"

