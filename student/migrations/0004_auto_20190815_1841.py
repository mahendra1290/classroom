# Generated by Django 2.2.4 on 2019-08-15 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_auto_20190815_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='comment',
            field=models.CharField(max_length=50),
        ),
    ]
