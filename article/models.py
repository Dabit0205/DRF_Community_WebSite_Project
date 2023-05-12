from django.db import models
from user.models import User

# Create your models here.


class Article(models.Model):
    """
    Article 모델입니다,
    author 필드는 User모델을 참조합니다, on_delete를 CASCADE로 변경하였습니다, user부분에서 user삭제를 비활성화로 처리하기에
    유저가 작성한 게시글은 남게 됩니다. 그렇기에 db에서 유저 정보가 삭제되는 상황에서 함께 삭제되도록 변경하였습니다.
    title(게시글제목),content(게시글내용),created_at(게시글생성일),updated_at(게시글수정일), likes (좋아요)
    필드로 구성되어있습니다.
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="like_articles")
    bookmarks = models.ManyToManyField(User, related_name="bookmarked_articles")

    def __str__(self):
        return str(self.title)
