from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import (
    UserSerializer,
    MyTokenObtainSerializer,
    UserSignOutSerializer,
)
from rest_framework.generics import get_object_or_404
from user.models import User


# Create your views here.
class UserSignUpAndOutView(APIView):
    """
    사용자가 회원가입 하거나 회원 탈퇴를 하기 위한 APIView이다.
    Post(가입)와 Delete(탈퇴) 요청만 받음.
    """

    # permission_classes = (IsExsistDeleteXorCreateOnly,)

    def post(self, request):
        """
        회원가입을 위해선 username, email, password, password2를 입력받아야한다.
        상태코드 201 / 생성된 유저 정보(username,email)반환
        옳지 않은 입력(필수 입력 필드 빼먹거나 비밀번호 불일치)일 시 400 / error 반환
        """
        user_serialized = UserSerializer(data=request.data)
        if user_serialized.is_valid():
            user_serialized.save()
            return Response(user_serialized.data, status=status.HTTP_201_CREATED)
        return Response(user_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        회원탈퇴를 위해 passoword를 입력받아 현재 로그인 중인 유저(request.user)와 비교 후
        일치하면 해당 유저의 is_active 값을 False로 바꾼다.
        상태코드 200 : 탈퇴성공
        상태코드 400 : 비밀번호 틀림
        """
        user = request.user
        user = get_object_or_404(User, id=user.id)
        serializer = UserSignOutSerializer(user, request.data)
        if serializer.is_valid():
            user.is_active = False
            user.save()
            return Response(
                {"message": "signout_success"}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtaionVeiw(TokenObtainPairView):
    """
    토큰 발급시 사용되는 view입니다.
    기본 제공되는 것을 상속하여 속성(serializer_class)을 다시 지정해 사용합니다.
    기본제공되는 시리얼라이저를 상속해 커스텀한 MyTokenObtainSerializer을 사용합니다.
    """

    serializer_class = MyTokenObtainSerializer
