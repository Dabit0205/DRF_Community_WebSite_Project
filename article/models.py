from django.db import models
from user.models import User

# Create your models here.


class Article(models.Model):
    """
    Article 모델입니다,
    author 필드는 User모델을 참조합니다, on_delete에 SET_NULL을 주어
    회원이 삭제되어도 게시글은 남습니다.
    title(게시글제목),content(게시글내용),created_at(게시글생성일),updated_at(게시글수정일)
    필드로 구성되어있습니다.
    """

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)
