# Generated by Django 4.2.4 on 2023-09-14 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_takequiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='takequiz',
            name='do_you_foresee_getting_a_FT_Job_in_next_6_years',
            field=models.CharField(blank=True, help_text='Do you Foresee getting a FT Job in next 6 years?', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='takequiz',
            name='is_capcity_to_save',
            field=models.CharField(blank=True, help_text='Do you have Capacity to Save?', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='takequiz',
            name='is_full_time',
            field=models.CharField(blank=True, help_text='Do you work Full Time?', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='takequiz',
            name='is_nz_permanent',
            field=models.CharField(blank=True, help_text='Are you Aus or NZ Permanent Resident?', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='takequiz',
            name='is_saving_50k',
            field=models.CharField(blank=True, help_text='Do you have savings of $50k or more?', max_length=200, null=True),
        ),
    ]
