from django.urls import path
from article import views

urlpatterns = [
    path("", views.ArticleView.as_view(), name="article_view"),
]
