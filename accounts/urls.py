from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)

from . import views
from .forms import UserPasswordResetConfirmForm, UserPasswordResetForm

app_name = 'accounts'

urlpatterns = [
    # registration
    path('login/', LoginView.as_view(template_name='accounts/registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('check_username/', views.check_username, name='check_username'),

    # password reset
    path(
        'password_reset/', 
        PasswordResetView.as_view(
            template_name='accounts/user/password_reset.html', 
            success_url=reverse_lazy('accounts:password_reset_done'),
            email_template_name='accounts/user/password_reset_email.html',
            form_class=UserPasswordResetForm
        ), name='password_reset'
    ),
    path(
        'password_reset/email_confirm/', 
        PasswordResetDoneView.as_view(
            template_name='accounts/user/password_reset_status.html'
        ), name='password_reset_done'
    ),
    path(
        'password_reset/<uidb64>/<token>/', 
        PasswordResetConfirmView.as_view(
            template_name='accounts/user/password_reset_confirm.html',
            success_url=reverse_lazy('accounts:password_reset_complete'),
            form_class=UserPasswordResetConfirmForm
        ), name='password_reset_confirm'
    ),
    path(
        'password_reset/complete/', 
        PasswordResetCompleteView.as_view(
            template_name='accounts/user/password_reset_status.html'
        ), name='password_reset_complete'
    ),

    # user profile
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
]