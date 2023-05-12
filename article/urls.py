from django.urls import path
from article import views

urlpatterns = [
   path("", views.ArticleView.as_view(), name="article_view"),
   path("<int:article_id>/",views.ArticleDetailView.as_view(),name="article_detail_view"),
   path("<int:article_id>/comment/",views.CommentView.as_view(),name="comment_view"),
   path("<int:article_id>/comment/<int:comment_id>/", views.CommentDetailView.as_view(),name="article_comment_detail_view"),
]
 