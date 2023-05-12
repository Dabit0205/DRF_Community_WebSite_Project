from django.urls import path
from article import views

urlpatterns = [
    path("", views.ArticleView.as_view(), name="article_view"),
    path(
        "<int:article_id>/",
        views.ArticleDetailView.as_view(),
        name="article_detail_view",
    ),
    path("feed/", views.FeedView.as_view(), name="feed"),
    path("<int:article_id>/like/", views.LikeView.as_view(), name="like_view"),
    path(
        "<int:article_id>/bookmark/", views.BookmarkView.as_view(), name="bookmark_view"
    ),
]
