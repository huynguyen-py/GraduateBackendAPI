from django.contrib import admin
from .models import Article, Comment, Report, ReportDetail


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = ('title', 'create_time', 'author_mail', 'status_ar')
    list_filter = ('category', 'create_time', 'status_ar')

    fieldsets = (
        (None, {'fields': ('author_ar', 'title', 'content'
        , 'category', 'users_like', 'status_ar')}),
    )

    def author_mail(self, obj):
        return obj.author_ar.email

    def category(self, obj):
        return obj.category.title_cat

    # To display only in list_display

    ordering = ['create_time', ]
    search_fields = ['author_ar__email']     # with direct foreign key no error but filtering not possible directly


class CommentAdmin(admin.ModelAdmin):
    model = Article
    list_display = ('article_cmt', 'user_cmt', 'create_date_cmt', 'reply_cmt')
    list_filter = ('create_date_cmt',)
    fieldsets = (
        (None, {'fields': ('user_cmt', 'article_cmt', 'content_cmt'
        , 'reply_cmt',)}),
    )

    def user_cmt(self, obj):
        return obj.user_cmt.email

    def article_cmt(self, obj):
        return obj.article_cmt.title

    def reply_cmt(self, obj):
        return obj.reply_cmt.email

    # To display only in list_display

    ordering = ['create_date_cmt', ]
    search_fields = ['user_cmt__email']     # with direct foreign key no error but filtering not possible directly


class ReportAdmin(admin.ModelAdmin):
    model = Report
    list_display = ('type_rp', 'warning_level', 'action_to_handle')
    list_filter = ('warning_level','action_to_handle')

    fieldsets = (
        (None, {'fields': ('type_rp', 'warning_level', 'action_to_handle')}),
    )


    # To display only in list_display

    ordering = ['warning_level', ]
    search_fields = ['warning_level']     # with direct foreign key no error but filtering not possible directly


class ReportDetailAdmin(admin.ModelAdmin):
    model = ReportDetail
    list_display = ('author_report', 'article_be_reported', 'type_reported', 'create_date', 'status_processing')
    list_filter = ('create_date', 'status_processing')

    fieldsets = (
        (None, {'fields': ('author_report', 'article_be_reported', 'type_reported', 'status_processing')}),
    )

    def author_report(self, obj):
        return obj.author_report.email

    def article_be_reported(self, obj):
        return obj.article_be_reported.title

    def type_reported(self, obj):
        return obj.type_reported.type_rp


    # To display only in list_display

    ordering = ['create_date', ]
    search_fields = ['author_report__email', 'article_be_reported__title']     # with direct foreign key no error but filtering not possible directly

admin.site.unregister(Article)
admin.site.register(Article, ArticleAdmin)
admin.site.unregister(Comment)
admin.site.register(Comment, CommentAdmin)
admin.site.unregister(Report)
admin.site.register(Report, ReportAdmin)
admin.site.unregister(ReportDetail)
admin.site.register(ReportDetail, ReportDetailAdmin)
