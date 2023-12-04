from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, UserUpdateView, PasswordRecoveryView, EmailVerificationView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('password_recovery/', PasswordRecoveryView.as_view(), name='password_recovery'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
]
