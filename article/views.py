from rest_framework import status, permissions
from rest_framework.decorators import APIView
from rest_framework.response import Response
from article.models import Article
from article.serializers import ArticleSerializer, ArticleCreateSerializer
from article.permissions import IsOwnerOrReadOnly

# Create your views here.


class ArticleView(APIView):
    """
    article/ url에서 사용됩니다.
    ArticleView는 모든 게시물 출력, 게시물 등록에 사용됩니다.
    get방식일 경우 저장된 모든 게시글을 보여줍니다,
    post방식을 사용하면 게시글을 등록할 수 있습니다.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        """
        objects.all()을 통해 모델에 저장된 모든 것을 가져옵니다.
        many=True를 사용하여 오류를 방지합니다.
        성공 시 상태메시지 200을 출력합니다.
        """
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        토큰에서 유저 정보를 받을 수 있기 때문에 수정되었습니다.
        data 부분에는 게시글의 title,content를 받아 valid 작업을 받습니다.
        context에는 request요청을 한 유저의 정보를 받습니다. author_id를 저장하기 위해 사용되었습니다.
        serializer를 통해 검증된 정보를 만들어 return시켜줍니다.
        """
        serializer = ArticleCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "작성완료"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    """
    ArticleDetailView에서는 게시글 상세보기, 게시글 수정, 게시글 삭제를 수행합니다.
    premission으로 준 IsOwnerOrReadOnly은 요청자가 게시글의 작성자일 경우와 아닐 경우를 판단하여
    권한을 부여합니다, 기본적으로 읽기 권한만을 주어 게시글을 관리합니다.
    article_id를 이용하여 대상을 지정하여 여러 메서드를 통해 기능을 동작합니다.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, article_id):
        """
        get 방식으로 접근 시 제시한 article_id의 게시글을 보여줍니다.
        """
        article = Article.objects.get(id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, article_id):
        """
        title, content를 받아 게시글을 수정합니다.
        IsOwnerOrReadOnly을 통해 권한을 부여합니다.
        알맞은 값을 넣으면 수정완료 메시지를 출력합니다, 그렇지 않을 경우 상태메시지 400을 출력합니다.
        """
        article = Article.objects.get(id=article_id)
        serializer = ArticleCreateSerializer(article, data=request.data)
        self.check_object_permissions(self.request, article)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "수정완료"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
