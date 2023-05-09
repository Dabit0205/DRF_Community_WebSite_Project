from django.urls import path
from user import views

urlpatterns = [
    path("sign/", views.UserSignUpAndOutView.as_view(), name="signup/out"),
]
