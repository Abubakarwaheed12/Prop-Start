# Generated by Django 4.2.4 on 2023-09-19 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_takequiz_do_you_foresee_getting_a_ft_job_in_next_6_years_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='takequiz',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]