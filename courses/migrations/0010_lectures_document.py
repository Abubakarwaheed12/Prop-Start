# Generated by Django 4.2.4 on 2023-11-20 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_alter_preorder_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='lectures',
            name='document',
            field=models.FileField(blank=True, help_text='please upload the document related video!', null=True, upload_to='course_documents'),
        ),
    ]
