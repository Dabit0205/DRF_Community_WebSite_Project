from rest_framework import status
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
        is_valid로 title과 content가 형식에 맞게 들어왔는지 확인합니다.
        통과 시 저장합니다, 토큰은 사용자를 인증하는데 사용됩니다,
        그렇기에 save 시 user정보가 담기지 않습니다, user를 따로 지정해주어,
        db에 저장될 때 요청한 user의 정보를 저장해야 합니다.
        생성에 성공하면 상태메시지 201을 그렇지 않을 경우 400을 출력합니다.
        """
        serializer = ArticleCreateSerializer(date=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "작성완료"}, serializer.data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
