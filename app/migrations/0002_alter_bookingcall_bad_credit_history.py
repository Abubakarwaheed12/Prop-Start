# Generated by Django 4.2.4 on 2023-09-02 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingcall',
            name='bad_credit_history',
            field=models.BooleanField(),
        ),
    ]
