# Generated by Django 4.2.4 on 2023-09-02 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_bookingcall_bad_credit_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingcall',
            name='bad_credit_history',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='bookingcall',
            name='is_resident',
            field=models.CharField(max_length=255),
        ),
    ]