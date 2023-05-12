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


class IsMeOrReadOnly(permissions.BasePermission):
    """
    프로필의 주인이 request.user와 같은 경우 PUT,PATCH,DELETE 메서드에 대한 권한을 허용
    이외의 요청자일 경우 읽기 권한만 허용
    """

    message = "권한이 없습니다"

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.username == request.user
