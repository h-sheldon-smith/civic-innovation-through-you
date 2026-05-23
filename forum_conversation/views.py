from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from vote.models import UP, DOWN
from machina.core.db.models import get_model

Post = get_model('forum_conversation', 'Post')

# toggle post's upvote status for the signed-in user
@login_required
@require_POST
def vote_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user_id = request.user.id

    if post.votes.exists(user_id, action=UP):
        # the user hasn't upvoted the post already
        post.votes.down(user_id) # removes the upvote (not Reddit-style)
        voted = False
    else:
        post.votes.up(user_id)
        voted = True

    return JsonResponse({
        'voted': voted,
        'score': post.votes.count(action=UP),
    })