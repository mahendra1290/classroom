# Generated by Django 2.2.4 on 2019-08-07 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_auto_20190807_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='my_classes',
            field=models.ManyToManyField(to='teacher.TeachersClassRoom'),
        ),
    ]
