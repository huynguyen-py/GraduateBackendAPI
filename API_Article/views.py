from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import Article, Comment, ReportDetail
from API_Source.models import User
from .serializers import ArticleSerializer, CommentSerializer, ReportSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user_cmt=self.request.user)

    # def get_queryset(self):
    #     return Comment.objects.filter(user_cmt=self.request.user).order_by('-create_date_cmt')
    #
    # @action(detail=True, methods=['post'])
    # def get_by_article(self, request, pk=None):
    #     article = Article.objects.get(pk=pk)
    #     lst_cmt = Comment.objects.get(article_cmt=article)
    #     comment_serializer = CommentSerializer(lst_cmt, many=True)
    #     return Response({'data': comment_serializer.data})

@api_view()
@permission_classes([permissions.IsAuthenticated,])
def get_comment_of_article_view(request):
    article = Article.objects.get(pk=request.query_params['id_article'])
    lst_cmt = Comment.objects.filter(article_cmt=article.id).order_by('-create_date_cmt')
    comment_serializer = CommentSerializer(lst_cmt, many=True)
    return Response({'data': comment_serializer.data})


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author_ar=self.request.user)

    def get_queryset(self):
        return Article.objects.all()

    def list(self, request):
        queryset = Article.objects.all().order_by('-create_time')
        serializer = ArticleSerializer(queryset, many=True)

        # print(serializer.data[1]["author_name"])
        # def SwapID2Name():
        #run = 0
        # for art in queryset:
        #     user = User.objects.filter(pk=art.author_ar.id)
        #     u_serializer = UserSerializer(user, many=True)
        #     # serializer.data[run]['author_ar'] = u_serializer.data[0]['username']
        #     serializer.data[run]
        #     run += 1
        # end swapID2Name

        return Response({'data': serializer.data})

    def destroy(self, request, pk=None):
        try:
            obj = Article.objects.filter(pk=pk)
            obj.delete()
        except Http404:
            return Response({"message": "Failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Detroyed"}, status=status.HTTP_200_OK)


@api_view()
@permission_classes([permissions.IsAuthenticated, ])
def getListArticleofUser(request):
    article = Article.objects.filter(author_ar=request.user)
    article_serializer = ArticleSerializer(article, many=True)
    return Response({'data': article_serializer.data})


@api_view()
@permission_classes([permissions.IsAuthenticated, ])
def getArticleByCategory(request):
    article = Article.objects.filter(category=request.query_params['id_cat'])
    article_serializer = ArticleSerializer(article, many=True)
    return Response({'data': article_serializer.data})

@api_view()
@permission_classes([permissions.IsAuthenticated, ])
def getArticleByTitle(request):
    string_s = str(request.query_params['key_search'])
    if "@" in string_s:
        user_ = get_object_or_404(User, email=string_s)
        article = Article.objects.filter(author_ar=user_)
    else:
        article = Article.objects.filter(title__contains=string_s)
    article_serializer = ArticleSerializer(article, many=True)
    return Response({'data': article_serializer.data})


@api_view()
@permission_classes([permissions.IsAuthenticated,])
def user_like_article(request):
    article = get_object_or_404(Article, id=request.query_params['id_article'])
    if article.users_like.filter(email=request.user).exists():
        article.users_like.remove(request.user)
        return Response({'data': "unliked"})
    else:
        article.users_like.add(request.user)
        return Response({'data': "liked"})


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author_report=self.request.user)

    def get_queryset(self):
        return ReportDetail.objects.filter(author_report=self.request.user).order_by('-create_date')

    def list(self, request):
        queryset = ReportDetail.objects.filter(author_report=self.request.user).order_by('-create_date')
        serializer = ReportSerializer(queryset, many=True)
        return Response({'data': serializer.data})

    def destroy(self, request, pk=None):
        try:
            obj = ReportDetail.objects.filter(pk=pk)
            obj.delete()
        except Http404:
            return Response({"message": "Failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Detroyed"}, status=status.HTTP_200_OK)

