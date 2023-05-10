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
    create를 오버라이딩하였습니다.
    title과 content에 검증된 값을 넣습니다,db에 author_idr값을 넣기위해 view에서 context를 이용하여 받은 유저의 정보에서 user.id만 뽑아 author_id에 넣습니다.
    """

    class Meta:
        model = Article
        fields = ("title", "content")

    def create(self, validated_data):
        article = Article.objects.create(
            title=validated_data["title"],
            content=validated_data["content"],
            author_id=self.context["request"].user.id,
        )
        return article
