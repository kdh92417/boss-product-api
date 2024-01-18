from django.urls import path

from app.views.user import SignupView

urlpatterns = [
    path("user/signup", SignupView.as_view(), name="signup"),
]
