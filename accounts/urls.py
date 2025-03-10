from django.urls import path
from .views import LoginView, LogoutView, SignUpView, UserListView, TestAuthView, UserProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserListView.as_view(), name='user-detail'),
    path('test-auth/', TestAuthView.as_view(), name='test-auth'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),
]