# Generated by Django 2.2.4 on 2019-08-12 10:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_merge_20190811_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='submission_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
