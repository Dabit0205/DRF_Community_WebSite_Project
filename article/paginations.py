from rest_framework.pagination import PageNumberPagination

"""
pagination을 커스텀 하거나, 필요한 곳에 지정하여 사용할 수 있습니다.
"""


class ArticlePagination(PageNumberPagination):
    """
    page_size는 한 페이지에 몇 개의 게시글을 담을지 결정합니다.
    page_query_param은 페이지의 이름을 나타냅니다.
    ex)http://127.0.0.1:8000/article/?page=2 를 사용하면 2페이지로 이동합니다.
    여기서 param을 "mypage"라고 지정한다면
    http://127.0.0.1:8000/article/?mypage=2 라고 사용해야합니다.
    max_page_size는 최대 페이지 수를 결정합니다.
    """

    page_size = 10
    page_query_param = "page"
    max_page_size = 100
