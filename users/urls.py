from django.contrib.auth.views import (
    LogoutView
)
from django.urls import path

from users.views import CustomLoginView, SignUpView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
