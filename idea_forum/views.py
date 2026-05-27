from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from vote.models import UP
from machina.core.db.models import get_model

Post = get_model('forum_conversation', 'Post')

# toggle post's upvote status for the signed-in user
@login_required
@require_POST
def toggle_post_upvote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user_id = request.user.id

    previously_upvoted = post.votes.exists(user_id, action=UP)

    if previously_upvoted:
        post.votes.delete(user_id)
    else:
        post.votes.up(user_id)

    upvoted_now = not previously_upvoted

    return JsonResponse({
        'user_upvoted': upvoted_now,
        'post_score': post.votes.count(action=UP),
    })