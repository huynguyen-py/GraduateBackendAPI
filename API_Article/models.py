from ckeditor.fields import RichTextField
from django.db import models
from API_Source.models import User
from django.utils import timezone
from django.contrib import admin
from API_Source.serializers import UserSerializer

STATUS_PROCESSING = (("approve", "approved"), ("pending", "pending"), ("reject", "rejected"))
ACTION_PROCESSING = (("remove", "removed"), ("notification", "notification"), ("reject", "rejected"))
TYPE_REPORT = (("Nudity", "Nudity"), ("Violence", "Violence")
               , ("Spam", "Spam"), ("Hate Speech", "Hate Speech")
               , ("Terrorism", "Terrorism"), ("Something Else", "Something Else"),
               )
PRIVACY = (("private", "private"), ("public", "public"))


class Category(models.Model):
    # title of category
    title_cat = models.TextField()
    # total article of each object category
    total_article = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title_cat}'


class Article(models.Model):
    # title of article/status
    title = models.CharField(max_length=255, blank=True, default="")
    # author of article/status
    author_ar = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Post_as_author")
    # date time created
    create_time = models.DateField(auto_now_add=True)
    # category of article/status example: skin, soft, head/neck,...
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # body of article/status
    content = RichTextField(null=True, blank=False, default="Body_article")
    # store user who liked article
    users_like = models.ManyToManyField(User, blank=True)
    # status of article as: approved, pending, reject
    status_ar = models.CharField(
        max_length=20,
        choices=STATUS_PROCESSING,
        default='pending'
    )

    def total_likes(self):
        return self.users_like.count()

    def list_liked(self):
        user_ser = UserSerializer(self.users_like.all(), many=True)
        lst_name_u = []
        for u in user_ser.data:
            lst_name_u.append(u['email'])
        return lst_name_u

    def list_followed(self):
        user_ser = UserSerializer(self.author_ar.Followed.all(), many=True)
        lst_name_u = []
        for u in user_ser.data:
            lst_name_u.append(u['email'])
        return lst_name_u

    def getNameAuthor(self):
        return self.author_ar.username


class Comment(models.Model):
    # user who write comment in bellow field article/status
    user_cmt = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_of_comment")
    # artile which be wrote comment by user field above
    article_cmt = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comment_on_article")
    # time created comment
    create_date_cmt = models.DateTimeField(default=timezone.datetime.now())
    # body/ content of this comment
    # content_cmt = RichTextField(null=True, blank=True, default="Body_comment")
    content_cmt = models.TextField(null=True, blank=True, default="Body_comment")
    # other comment which reply self comment
    reply_cmt = models.ManyToManyField("self", blank=True, related_name="comment_reply_comment")


    def getNameAuthor(self):
        return self.user_cmt.email

    def getDateComment(self):
        return  self.create_date_cmt.date()
    #
    # def total_likes(self):
    #     return self.user_cmt.count()


class Report(models.Model):
    # set type or describe of this report
    type_rp = models.CharField(
        max_length=50,
        choices=TYPE_REPORT,
        default="Something Else"
    )
    # set level warning
    warning_level = models.IntegerField()
    # action will apply for handle this report
    action_to_handle = models.CharField(
        max_length=50,
        choices=ACTION_PROCESSING,
        default="notification"
    )

    def __str__(self):
        return f'{self.type_rp}'


class ReportDetail(models.Model):
    # author of report
    author_report = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_report_article")
    # article be reported by above author field
    article_be_reported = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_be_reported")
    # type reported
    type_reported = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="type_of_report")
    # date
    create_date = models.DateField(auto_now_add=True)
    # is handled ? or not ? and handle by action?
    status_processing = models.CharField(
        max_length=20,
        choices=STATUS_PROCESSING,
        default='pending'
    )


class GroupUser(models.Model):
    name_of_group = models.CharField(max_length=255, blank=False)
    admin_group = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_of_this_group")
    privacy_group = models.CharField(
        max_length=20,
        choices=PRIVACY,
        default='public'
    )
    # member of this group
    member_group = models.ManyToManyField(User, related_name="member_of_group")
    article_group = models.ManyToManyField(Article, related_name="article_of_group")


admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Report)
admin.site.register(ReportDetail)
# admin.site.register(GroupUser)

