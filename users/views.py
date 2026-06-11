from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import OuterRef, Subquery, IntegerField
from datetime import timedelta
from .models import UserModeration
from gamification.models import UserPoints
from gamification import game_services as gamification_services, game_choices as gamification_choices


# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('index')  # Redirect to the home page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            try:
                mod = user.moderation
                if mod.is_banned():
                    return render(request, 'users/login.html', {
                        'form': form,
                        'punishment': {
                            'type': 'banned',
                            'reason': mod.reason,
                        },
                    })
                if mod.is_suspended():
                    until = mod.suspended_until
                    return render(request, 'users/login.html', {
                        'form': form,
                        'punishment': {
                            'type': 'suspended',
                            'reason': mod.reason,
                            'until': until.strftime('%B %d, %Y at %I:%M %p') if until else None,
                        },
                    })
                if mod.is_muted():
                    login(request, user)
                    until = mod.mute_until
                    request.session['mute_popup'] = {
                        'reason': mod.reason,
                        'until': until.strftime('%B %d, %Y at %I:%M %p') if until else None,
                    }
                    login(request, user)
                    gamification_services.award_points(user, gamification_choices.PointType.LOGIN)
                    return redirect('users:mute_notice')
            except Exception as e:
                print("LOGIN MODERATION ERROR: ", e, flush=True)
                pass
            login(request, user)
            gamification_services.award_points(user, gamification_choices.PointType.LOGIN)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def account_settings_view(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=405)

    email = request.POST.get('email', '').strip()

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'success': False, 'error': 'Enter a valid email address.'})

    if User.objects.exclude(pk=request.user.pk).filter(email=email).exists():
        return JsonResponse({'success': False, 'error': 'That email is already in use.'})

    request.user.email = email
    request.user.save(update_fields=['email'])
    return JsonResponse({'success': True})


@login_required
def mute_notice_view(request):
    mute_popup = request.session.pop('mute_popup', None)
    return render(request, 'users/mute_notice.html', {'mute_popup': mute_popup})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')  # Redirect to the home page after logout
    return render(request, 'users/logout.html')


@permission_required('users.can_admin_site', raise_exception=True)
def account_list_view(request):
    sort = request.GET.get('sort', 'username')
    search = request.GET.get('search', '').strip()

    points_subquery = Subquery(
        UserPoints.objects.filter(resident=OuterRef('pk'), point_type='Grand Total').values('total_points')[:1],
        output_field=IntegerField()
    )

    users = User.objects.select_related('moderation').exclude(is_superuser=True).annotate(total_points=points_subquery)

    if search:
        users = users.filter(username__icontains=search)

    users = users.order_by(sort)
    return render(request, 'users/admin_account_list.html', {
        'users': users,
        'sort': sort,
        'search': search,
    })


@permission_required('users.can_admin_site', raise_exception=True)
def account_detail_view(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    mod, _ = UserModeration.objects.get_or_create(user=target_user)
    return render(request, 'users/admin_account_detail.html', {
        'target_user': target_user,
        'mod': mod,
    })


@permission_required('users.can_admin_site', raise_exception=True)
def moderate_user_view(request, pk):
    if request.method != 'POST':
        return redirect('users:account_detail', pk=pk)

    target_user = get_object_or_404(User, pk=pk)
    mod, _ = UserModeration.objects.get_or_create(user=target_user)

    action = request.POST.get('action')
    reason = request.POST.get('reason', '').strip()
    duration = request.POST.get('duration', '').strip()

    def parse_duration(value):
        try:
            amount, unit = value.split()
            amount = int(amount)
            if unit.startswith('hour'):
                return timedelta(hours=amount)
            elif unit.startswith('day'):
                return timedelta(days=amount)
            elif unit.startswith('week'):
                return timedelta(weeks=amount)
        except (ValueError, AttributeError):
            return None

    if action == 'mute':
        delta = parse_duration(duration)
        if not delta:
            messages.error(request, "Invalid duration for mute.")
            return redirect('users:account_detail', pk=pk)
        mod.status = 'muted'
        mod.mute_until = timezone.now() + delta
        mod.suspended_until = None

    elif action == 'suspend':
        delta = parse_duration(duration)
        if not delta:
            messages.error(request, "Invalid duration for suspension.")
            return redirect('users:account_detail', pk=pk)
        mod.status = 'suspended'
        mod.suspended_until = timezone.now() + delta
        mod.mute_until = None

    elif action == 'ban':
        mod.status = 'banned'
        mod.mute_until = None
        mod.suspended_until = None

    elif action == 'restore':
        mod.status = 'active'
        mod.mute_until = None
        mod.suspended_until = None
        reason = reason or 'Restored to active'

    else:
        messages.error(request, "Unknown action.")
        return redirect('users:account_detail', pk=pk)

    mod.reason = reason
    mod.actioned_by = request.user
    mod.save()

    messages.success(request, f"{target_user.username} has been {action}d successfully.")
    return redirect('users:account_list')