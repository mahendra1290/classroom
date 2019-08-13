# Generated by Django 2.2.4 on 2019-08-13 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('instructions', models.CharField(max_length=100)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('pub_date', models.DateField(auto_now=True, null=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.TeachersClassRoom')),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentsFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='assignment/files/')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignment.Assignment')),
            ],
        ),
    ]
