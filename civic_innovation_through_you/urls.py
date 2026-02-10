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

from . import views

urlpatterns = [
<<<<<<< HEAD
    path('admin/', admin.site.urls), #path for admin dashboard
    path('idea/', include('idea_suggestion.urls')) #path for idea_suggestions app
=======
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
<<<<<<< HEAD
    path('ideas/', include('idea_suggestion.urls')) #path for idea_suggestions app
>>>>>>> main
=======
    path('idea/', include('idea_suggestion.urls')) # path for idea_suggestions app
>>>>>>> 4069a29 (revised static folder to remove nesting folders. Revised so idea submit questions populate in the idea pop up. Updated Resident_Idea_submission_View, made resident_form to create the pop up contents, made idea_resident template to populate into pop up, updated Idea Submission Pop Up section in the navbar, created context processor and added it to settings. TODO: Remove close button, add submit button on idea pop up.)
]
