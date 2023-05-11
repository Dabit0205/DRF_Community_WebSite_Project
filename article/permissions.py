from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    BasePermission을 상속받아 만들었습니다.
    게시글의 작성자가 request.user와 같은 경우 PUT,PATCH,DELETE 메서드에 대한 권한을 허용합니다.
    이외의 요청자일 경우 읽기 권한만 허용됩니다.
    권한이 없을 경우 message를 오버라이딩하여 권한이 없습니다 가 출력됩니다.
    """

    message = "권한이 없습니다"

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.author == request.user
