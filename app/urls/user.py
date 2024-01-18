from django.urls import path

from app.views.user import SignupView, LoginView, LogoutView

urlpatterns = [
    path("user/signup", SignupView.as_view(), name="signup"),
    path("user/login", LoginView.as_view(), name="login"),
    path("user/logout", LogoutView.as_view(), name="logout"),
]
