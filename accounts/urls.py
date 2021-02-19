from django.urls import path
from .views import SignUpView, UserDetailView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('users/<username>', UserDetailView.as_view(), name='user-detail')
]
