from rest_framework import permissions


class SignOutAuthenticatedOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        POST 요청(회원가입)만은 비회원이라도 가능해야하므로 무조건 True
        이외에는 로그인한 유저 본인의 정보에 대한 것이므로 로그인 여부를 확인한다.
        """
        if request.method == "POST":
            return True
        return bool(request.user and request.user.is_authenticated)
