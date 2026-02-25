from django.shortcuts import render
# from django.http import JsonResponse
# from django.contrib.auth import login_required

from machina.apps.forum.models import Forum

def Idea_Forum_View(request):
    return render(request, 'forum.html')

def BoardBase_View(request):
    forums = Forum.objects.all()

    return render(request, 'machina/board_base_foo.html', {"forums": forums})