# Generated by Django 4.1.4 on 2023-09-12 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_rename_instructor_cousre_instructor'),
    ]

    operations = [
        migrations.AddField(
            model_name='cousre',
            name='price',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
