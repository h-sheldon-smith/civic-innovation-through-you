from machina.core.db.models import get_model

Post = get_model('forum_conversation', 'Post')


def get_a_post_id_from_mod_queue():
    return post_id

def get

# copied functionality from machina.apps.forum_moderation.views.PostApproveView.approve(...)
def approve_post(post_id):
    post = Post.objects.get(pk=post_id)
    post

# copied functionality from machina.apps.forum_moderation.views.PostDisapproveView.disapprove(...)
def disapprove_post(post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()

