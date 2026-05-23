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
def toggle_upvote_post(request, post_id):
    return _vote_post(request, post_id, True)

# toggle post's downvote status for the signed-in user
@login_required
@require_POST
def toggle_downvote_post(request, post_id):
    return _vote_post(request, post_id, False)

@login_required
@require_POST
def _vote_post(request, post_id, is_upvote):
    post = get_object_or_404(Post, pk=post_id)
    user_id = request.user.id

    if is_upvote:
        action=UP
    else:
        action=DOWN

    if post.votes.exists(user_id, action=action):
        # the user hasn't upvoted/downvoted the post already
        post.votes.delete(user_id)
        voted = False
    else:
        # delete user's existing vote first, to handle cases of both prexisting and not opposite vote
        post.votes.delete(user_id)

        if is_upvote:
            post.votes.up(user_id)
        else:
            post.votes.down(user_id)
        voted = True

    return JsonResponse({
        'voted': voted,
        'score': post.votes.count(action=action),
        'vote_type': action,
    })