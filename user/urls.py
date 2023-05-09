from django.urls import path
from user import views
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path("sign/", views.UserSignUpAndOutView.as_view(), name="signup/out"),
    path("token/", views.MyTokenObtaionVeiw.as_view(), name="token"),
]
