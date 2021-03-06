# Generated by Django 3.1.7 on 2021-03-07 06:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('API_Article', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='reportdetail',
            name='author_report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_report_article', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reportdetail',
            name='type_reported',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_of_report', to='API_Article.report'),
        ),
        migrations.AddField(
            model_name='groupuser',
            name='admin_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_of_this_group', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='groupuser',
            name='article_group',
            field=models.ManyToManyField(related_name='article_of_group', to='API_Article.Article'),
        ),
        migrations.AddField(
            model_name='groupuser',
            name='member_group',
            field=models.ManyToManyField(related_name='member_of_group', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='article_cmt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_on_article', to='API_Article.article'),
        ),
        migrations.AddField(
            model_name='comment',
            name='reply_cmt',
            field=models.ManyToManyField(blank=True, related_name='_comment_reply_cmt_+', to='API_Article.Comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user_cmt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_of_comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='author_ar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Post_as_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_Article.category'),
        ),
        migrations.AddField(
            model_name='article',
            name='users_like',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
