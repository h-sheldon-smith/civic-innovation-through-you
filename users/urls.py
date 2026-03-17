from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/accounts/', views.account_list_view, name='account_list'),
    path('admin/accounts/<int:pk>/', views.account_detail_view, name='account_detail'),
    path('admin/accounts/<int:pk>/moderate/', views.moderate_user_view, name='moderate_user'),
]