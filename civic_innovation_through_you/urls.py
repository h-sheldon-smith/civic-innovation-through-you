"""
URL configuration for civic_innovation_through_you project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from machina import urls as machina_urls
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('ideas/', include('idea_suggestion.urls')), # path for idea_suggestions app
    path('users/', include('users.urls')), # path for users app
    path('forum/', include(machina_urls)), # path for machina package
    path('avatar/', include('avatar.urls')), # path for avatar package
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
