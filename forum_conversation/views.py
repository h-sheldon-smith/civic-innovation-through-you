from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from machina.core.db.models import get_model

Post = get_model('forum_conversation', 'Post')

# like or unlike the post
@login_required
@require_POST
def vote_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user_id = request.user.id

    # if the user hasn't voted already
    if post.votes.exists(user_id):
        post.votes.down(user_id) # removes the upvote (not Reddit-style)
        voted = False
    else:
        post.votes.up(user_id)
        voted = True

    return JsonResponse({
        'user_voted': voted,
        'post_total_votes': post.vote_count,
    })