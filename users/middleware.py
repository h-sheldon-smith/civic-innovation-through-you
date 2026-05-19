import logging

from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone

from users.models import UserModeration

logger = logging.getLogger(__name__)

EXEMPT_URLS = {'/users/login/', '/users/logout/', '/users/register/'}

# URL prefixes where POST is blocked for muted users
POSTING_PREFIXES = ('/forum/',)


class ModerationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path not in EXEMPT_URLS:
            try:
                mod = request.user.moderation
            except UserModeration.DoesNotExist:
                return self.get_response(request)
            except Exception:
                logger.exception("ModerationMiddleware: unexpected error fetching moderation for user %s", request.user.pk)
                return self.get_response(request)

            try:
                if mod.is_banned():
                    logout(request)
                    messages.error(request, "Your account has been permanently banned.")
                    return redirect('/users/login/')

                if mod.is_suspended():
                    logout(request)
                    until = mod.suspended_until
                    msg = "Your account is suspended"
                    if until:
                        msg += f" until {until.strftime('%B %d, %Y at %I:%M %p %Z')}"
                    msg += "."
                    messages.error(request, msg)
                    return redirect('/users/login/')

                if mod.is_muted() and request.method == 'POST':
                    if any(request.path.startswith(p) for p in POSTING_PREFIXES):
                        until = mod.mute_until
                        msg = "You are muted and cannot post"
                        if until:
                            msg += f" until {until.strftime('%B %d, %Y at %I:%M %p %Z')}"
                        msg += "."
                        messages.error(request, msg)
                        return redirect(request.META.get('HTTP_REFERER', '/'))

            except Exception:
                logger.exception("ModerationMiddleware: unexpected error during moderation check for user %s", request.user.pk)

        return self.get_response(request)
