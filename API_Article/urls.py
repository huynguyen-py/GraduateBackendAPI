from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CommentViewSet, get_comment_of_article_view, user_like_article\
                    , ReportViewSet, getListArticleofUser, getArticleByCategory, getArticleByTitle

router = DefaultRouter()
router.register(r'article', ArticleViewSet, basename='article')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'reports', ReportViewSet, basename='report')
urlpatterns = [
    path('', include(router.urls)),
    path('get_comment/', get_comment_of_article_view, name="get_comment"),
    path('list_article/', getListArticleofUser, name="get_article_of_user"),
    path('list_by_category/', getArticleByCategory, name="get_article_by_category"),
    path('search/', getArticleByTitle, name="get_article_by_category"),
    path('like/', user_like_article, name="like_article"),
]
