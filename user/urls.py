from django.urls import path
from user import views
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path("sign/", views.UserSignUpAndOutView.as_view(), name="signup/out"),
    path("token/", views.MyTokenObtaionVeiw.as_view(), name="token"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    # refresh /access token이 expire하지 않았는지 post 메소드로 request body에 실어 확인.
    # {"token":"<토큰문자열>"} -> 유효할시 상태코드 200, 아닐시 401
    path("verify/", TokenVerifyView.as_view(), name="verify"),
    path("<int:user_id>/", views.ProfileView.as_view(), name="profile"),
]
