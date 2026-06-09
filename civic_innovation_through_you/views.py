from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from gamification import game_services as gamification_services, game_choices as gamification_choices
from gamification.models import UserPoints

def index(request):
    context = {}
    if request.user.is_authenticated:
        context['point_breakdown'] = UserPoints.objects.filter(
            resident=request.user
        ).exclude(point_type=gamification_choices.PointType.GRAND_TOTAL)
        context['user_points'] = gamification_services.get_points_by_user(
            request.user, gamification_choices.PointType.GRAND_TOTAL
        )
        context['user_badges'] = gamification_services.get_user_badges(request.user)
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

def health_check(request):
    return HttpResponse("healthy")