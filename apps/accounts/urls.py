from django.urls import path
from apps.accounts.views import UserRegisterView, LoginView, LogoutView, UserProfileView, UserEditProfileView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserEditProfileView.as_view(), name='edit-profile'),
]