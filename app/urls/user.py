from django.urls import path

from app.views.user import SignupView, LoginView, LogoutView

urlpatterns = [
    path("users/signup", SignupView.as_view(), name="signup"),
    path("users/login", LoginView.as_view(), name="login"),
    path("users/logout", LogoutView.as_view(), name="logout"),
]
