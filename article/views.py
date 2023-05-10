from rest_framework import status, permissions
from rest_framework.decorators import APIView
from rest_framework.response import Response
from article.models import Article
from article.serializers import ArticleSerializer, ArticleCreateSerializer

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
