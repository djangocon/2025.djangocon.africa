"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path("", include("website.urls")),
    path("accounts/", include("allauth.urls")),
    path("proposals/", include("proposals.urls")),
    path("sponsors/", include("sponsors.urls")),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('i18n/', include('django.conf.urls.i18n')),
]

# Media and static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("", include("website.urls")),
    path("accounts/", include("allauth.urls")),
    path("proposals/", include("proposals.urls")),
    path("sponsors/", include("sponsors.urls")),
    path("admin/", admin.site.urls),
)