from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import (
    UserSerializer,
    MyTokenObtainSerializer,
    UserSignOutSerializer,
    UserEditSerializer,
    ProfileSerializer,
    ProfileEditSerializer,
)
from user.permissions import SignOutAuthenticatedOnly, IsMeOrReadOnly
from rest_framework.generics import get_object_or_404
from user.models import User, Profile
from django.db.models.query_utils import Q


# Create the_userr views here.
class UserSignUpAndOutView(APIView):
    """
    사용자가 회원가입 하거나 회원 탈퇴를 하기 위한 APIView이다.
    Post(가입)와 Delete(탈퇴) 요청만 받음.
    """

    permission_classes = (SignOutAuthenticatedOnly,)

    def post(self, request):
        """
        회원가입을 위해선 username, email, password, password2를 입력받아야한다.
        상태코드 201 / 생성된 유저 정보(username,email)반환
        옳지 않은 입력(필수 입력 필드 빼먹거나 비밀번호 불일치)일 시 400 / error 반환
        """
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        회원탈퇴를 위해 passoword를 입력받아 현재 로그인 중인 유저(request.user)와 비교 후
        일치하면 해당 유저의 is_active 값을 False로 바꾼다.
        상태코드 200 : 탈퇴성공
        상태코드 400 : 비밀번호 틀림
        상태코드 401 : 만료토큰/로그인안함
        """
        user = request.user
        user = get_object_or_404(User, id=user.id)
        serializer = UserSignOutSerializer(user, request.data)
        if serializer.is_valid():
            user.is_active = False
            user.save()
            return Response({"message": "signout_success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """
        회원정보 변경을 위해 current_passoword를 입력받아 현재 로그인 중인 유저(request.user)와 비교 후
        일치하면 해당 유저의 정보(password...)를 수정한다.
        """
        user = get_object_or_404(User, id=request.user.id)
        serialized = UserEditSerializer(user, request.data, partial=True)
        if serialized.is_valid():
            serialized.save()
            return Response({"message": "변경성공"}, status=status.HTTP_200_OK)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        로그인한 유저 본인의 정보(이메일,아이디, 추후 추가될 수 있는 필드들)를 가져온다.
        """
        user = get_object_or_404(User, id=request.user.id)
        serialized = UserEditSerializer(user)
        return Response(serialized.data, status=status.HTTP_200_OK)


class MyTokenObtaionVeiw(TokenObtainPairView):
    """
    토큰 발급시 사용되는 view입니다.
    기본 제공되는 것을 상속하여 속성(serializer_class)을 다시 지정해 사용합니다.
    기본제공되는 시리얼라이저를 상속해 커스텀한 MyTokenObtainSerializer을 사용합니다.
    """

    serializer_class = MyTokenObtainSerializer


class ProfileView(APIView):
    """
    프로필 수정 및 조회를 위한 뷰
    """

    permission_classes = [IsMeOrReadOnly]

    def get(self, request, user_id):
        """
        프로필 조회
        username, email, image, bio, created_at, updated_at, articles
        탈퇴한 사용자는 조회할 수 없다.
        """
        profile = get_object_or_404(Profile, username=user_id)
        if not profile.username.is_active:
            return Response({"message": "탈퇴한 사용자입니다"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serialized = ProfileSerializer(profile)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        """
        프로필 수정
        bio와 image만 수정가능하다.
        """
        profile = get_object_or_404(Profile, username=user_id)
        self.check_object_permissions(request, profile)
        serialized = ProfileEditSerializer(profile, data=request.data, partial=True)
        if serialized.is_valid():
            serialized.save()
            return Response({"message": "edit success"}, status=status.HTTP_200_OK)


class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        the_user = get_object_or_404(User, id=user_id)
        if the_user == request.user:
            return Response("Can't self follow", status=status.HTTP_400_BAD_REQUEST)
        if the_user in request.user.followings.all():
            request.user.followings.remove(the_user)
            return Response("Unfollow", status=status.HTTP_200_OK)
        else:
            request.user.followings.add(the_user)
            return Response("Follow", status=status.HTTP_200_OK)
