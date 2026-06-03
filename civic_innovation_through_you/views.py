from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def index(request):
    context = {}
    if request.user.has_perm('users.can_admin_site'):
        from forum_conversation.models import Topic
        top_topics = (
            Topic.objects
            .select_related('forum', 'last_post')
            .filter(approved=True)
            .order_by('-posts_count', '-views_count')[:10]
        )
        context['top_topics'] = top_topics
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')