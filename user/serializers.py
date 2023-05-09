from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
import re

PASSWORD_REGEX = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,32}$"
USERNAME_REGEX = "^[A-Za-z\d]+[A-Za-z\d_\-@]{5,31}$"


class UserSerializer(serializers.ModelSerializer):
    """
    유저를 생성하거나 유저정보를 조회하기 위해 쓰이는 serializer이다.
    생성할 땐 password,password2,username,email을 받고
    조회할땐 username, email을 표시한다.

    """

    # 입력할 때만 쓰이는 password2 시리얼라이저필드 새로 정의
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            # write_only : 해당 필드를 쓰기 전용으로 만들어 준다.
            # 쓰기 전용으로 설정 된 필드는 직렬화 된 데이터에서 보여지지 않는다.
            "password": {"write_only": True},  # default : False
        }

    def create(self, validated_data):
        """
        부모 클래스의 create를 오버라이딩한다.
        검증이후 실행됨
        """
        # 저장할 때는 모델에 password2 필드가 없으므로 제거
        del validated_data["password2"]
        user = super().create(validated_data)
        user.set_password(validated_data["password"])  # 비밀번호 저장(해쉬)
        user.save()
        return user

    def validate(self, attrs):
        """
        부모 클래스의 validate 오버라이딩
        passwor와 password2가 일치하는지 확인
        이외 나머지 검증은 부모 클래스의 validate에 맡김
        """
        if attrs.get("password") != attrs.get("password2"):
            raise serializers.ValidationError({"password": "두 비멀번호가 일치하지 않습니다."})

        if not re.match(PASSWORD_REGEX, attrs.get("password")):
            raise serializers.ValidationError(
                {
                    "password": "비밀번호는 8자리~32자리, 한개 이상의 숫자/알파벳/특수문자(@,$,!,%,*,#,?,&)로 이루어져야합니다."
                }
            )
        if not re.match(USERNAME_REGEX, attrs.get("username")):
            raise serializers.ValidationError(
                {
                    "username": "길이 6자리 ~32자리, 알파벳으로 시작하고 알파벳 대소문자와 숫자, 특수기호 -,_,@ 로 이루어져야합니다."
                }
            )
        return super().validate(attrs)


class MyTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email

        return token
