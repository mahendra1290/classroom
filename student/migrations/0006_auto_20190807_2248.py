# Generated by Django 2.2.4 on 2019-08-07 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_auto_20190807_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='my_classes',
            field=models.ManyToManyField(blank=True, to='teacher.TeachersClassRoom'),
        ),
    ]
