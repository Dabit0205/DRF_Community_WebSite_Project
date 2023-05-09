from rest_framework import serializers
from article.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """
    article/ url에 GET방식일 때 사용합니다.
    article db에 저장된 모든 게시글을 보여줍니다.
    """

    class Meta:
        model = Article
        fields = "__all__"


class ArticleCreateSerializer(serializers.ModelSerializer):
    """
    article/ url에 POST방식일 때 사용합니다.
    게시글을 작성할 때 사용합니다, title과 content 값이 필요합니다.
    """

    class Meta:
        model = Article
        fields = ("title", "content")
