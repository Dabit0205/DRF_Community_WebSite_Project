from rest_framework import serializers
from article.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """
    article/ url에 GET방식일 때 사용합니다.
    article db에 저장된 모든 게시글을 보여줍니다.
    """

    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        """
        게시글을 출력할 때 int형태의 author_id가 아닌 회원가입 시 생성한 username 출력
        """
        return obj.author.username

    class Meta:
        model = Article
        fields = "__all__"


class ArticleListSerializer(serializers.ModelSerializer):
    """
    전체 게시글을 확인하기 위해 만들었습니다.
    제목, 작성자, 좋아요 수, 생성일을 표시합니다 + comment 추가 시 comment 수도 출력예정
    """

    author = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    """
    이후 count 추가 시 사용됩니다.
    """

    # comment_count = serializers.SerializerMethodField()
    def get_author(self, obj):
        """
        게시글을 출력할 때 int형태의 author_id가 아닌 회원가입 시 생성한 username 출력
        """
        return obj.author.username

    def get_likes_count(self, obj):
        """
        게시글에서 like의 수를 int형태로 출력합니다.
        """
        return obj.likes.count()

    # def get_comment_count(self, obj):
    """
    comment 추가 시 댓글의 수를 int형태로 출력합니다.
    """
    #     return obj.comment_set.count()

    class Meta:
        model = Article
        fields = ("title", "author", "likes_count", "created_at")


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
