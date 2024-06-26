# Generated by Django 4.2.4 on 2024-01-25 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_remove_usercourse_course_remove_usercourse_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lectures',
            name='video',
        ),
        migrations.RemoveField(
            model_name='lectures',
            name='video_url',
        ),
        migrations.RemoveField(
            model_name='premium_course',
            name='video',
        ),
        migrations.RemoveField(
            model_name='premium_course',
            name='video_url',
        ),
        migrations.AddField(
            model_name='lectures',
            name='url_1',
            field=models.URLField(default='https://www.youtube.com/watch?v=5qap5aO4i9A', help_text='please enter the url of the video'),
        ),
        migrations.AddField(
            model_name='lectures',
            name='url_2',
            field=models.URLField(blank=True, help_text='please enter the url of the video', null=True),
        ),
        migrations.AddField(
            model_name='lectures',
            name='url_3',
            field=models.URLField(blank=True, help_text='please enter the url of the video', null=True),
        ),
        migrations.AddField(
            model_name='premium_course',
            name='url_1',
            field=models.URLField(default='https://www.youtube.com/watch?v=5qap5aO4i9A', help_text='please enter the url of the video'),
        ),
        migrations.AddField(
            model_name='premium_course',
            name='url_2',
            field=models.URLField(blank=True, help_text='please enter the url of the video', null=True),
        ),
        migrations.AddField(
            model_name='premium_course',
            name='url_3',
            field=models.URLField(blank=True, help_text='please enter the url of the video', null=True),
        ),
    ]
