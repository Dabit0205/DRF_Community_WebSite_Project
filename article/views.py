from rest_framework import status, permissions
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import generics
from article.models import Article
from article.serializers import ArticleSerializer, ArticleCreateSerializer
from article.permissions import IsOwnerOrReadOnly
from article.paginations import ArticlePagination


# Create your views here.


class ArticleView(generics.ListCreateAPIView):
    """
    APIview에서는 페이지네이션 기능을 사용할 수 없었습니다, 그렇기에 generics를 사용했습니다.
    ListCreateAPIView는 GET요청일 때 조회, POST요청일 때 새로운 데이터를 생성하는 역할을 합니다.
    def get의 역할을 ListCreateAPIView에서 지원하기에 따로 지정해 줄 필요가 없습니다.
    queryset을 통해 article의 내용을 가져옵니다.
    필요한 것을 명시해주면 간단히 get 요청을 구현할 수 있습니다.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    paginations_class = ArticlePagination
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def post(self, request, *args, **kwargs):
        """
        토큰에서 유저 정보를 받을 수 있기 때문에 수정되었습니다.
        data 부분에는 게시글의 title,content를 받아 valid 작업을 받습니다.
        context에는 request요청을 한 유저의 정보를 받습니다. author_id를 저장하기 위해 사용되었습니다.
        serializer를 통해 검증된 정보를 만들어 return시켜줍니다.

        +)형태의 변화는 없지만 ListCreateAPIView를 사용했기에
        CreateAPIView를 오버라이딩 되었습니다.
        부모클래스를 상속하기에 *args, **kwargs를 추가하여 오류를 예방하고
        코드의 유연성을 높였습니다.
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

    def delete(self, request, article_id):
        """
        게시글을 삭제하는 기능을 합니다.
        게시글 작성자와 요청자를 비교하여 같다면 delete권한을 부여합니다.
        권한이 없을 경우 권한이 없습니다 메시지가 출력됩니다.
        삭제가 완료되면 삭제완료 메시지와 상태메시지 204가 출력됩니다.
        """
        article = Article.objects.get(id=article_id)
        self.check_object_permissions(self.request, article)
        article.delete()
        return Response({"message": "삭제완료"}, status=status.HTTP_204_NO_CONTENT)
