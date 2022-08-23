from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import register_view, UsersView, UserDetailView, UserChangeView, UserPasswordChangeView

app_name = 'accounts'
urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/create/', register_view, name='register_view'),
    path('accounts/users/', UsersView.as_view(), name='UsersView'),
    path('accounts/user/<int:pk>', UserDetailView.as_view(), name='UserDetailView'),
    path('<int:pk>/change/', UserChangeView.as_view(), name='UserChangeView'),
    path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),
]
