from API_Source.models import User
from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags
from rest_framework import serializers
from .models import Article, Comment, ReportDetail
from rest_framework.authtoken.models import Token


class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField('getAuthorName')
    users_like = serializers.SerializerMethodField('countLike')
    list_liked = serializers.SerializerMethodField('list_liked')
    list_followed = serializers.SerializerMethodField('list_followed')
    user_avatar = serializers.SerializerMethodField('getAvatar')

    def getAuthorName(self, Article):
        user_ = User.objects.get(id=Article.author_ar.id)
        return user_.email

    def getAvatar(self, Article):
        user_ = User.objects.get(id=Article.author_ar.id)
        return user_.avatar.url

    def countLike(self, Article):
        return Article.total_likes()

    def list_liked(self, Article):
        return Article.list_liked()

    def list_followed(self, Article):
        return Article.list_followed()

    class Meta:
        model = Article
        fields = ['id', 'title', 'create_time', 'category', 'content', 'status_ar',
                  'author_name', 'users_like', 'list_liked', 'user_avatar', 'list_followed']
        read_only_fields = ['id', 'status_ar', 'list_liked']
        extra_kwargs = {
            'content': {
                'required': True,
            }
        }
    #
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['content'] = strip_tags(instance.content)
    #     return data


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField('getAuthorName')
    date_create = serializers.SerializerMethodField('getDate')
    def getAuthorName(self, Comment):
        return Comment.getNameAuthor()

    def getDate(self, Comment):
        return Comment.getDateComment()

    class Meta:
        model = Comment
        fields = ['id', 'article_cmt', 'content_cmt', 'author_name', 'date_create']
        read_only_fields = ['id', 'create_date_cmt', 'author_name', 'date_create']
        extra_kwargs = {
            'content_cmt': {
                'required': True,
            }
        }


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportDetail
        fields = ['id', 'article_be_reported', 'type_reported', 'author_report', 'status_processing', 'create_date']
        read_only_fields = ['id', 'author_report', ]
        extra_kwargs = {
            'content_cmt': {
                'required': True,
            }
        }