from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import UserSerializer, MyTokenObtainSerializer


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


class MyTokenObtaionVeiw(TokenObtainPairView):
    serializer_class = MyTokenObtainSerializer
