# Generated by Django 2.2.4 on 2019-08-04 11:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(blank=True, choices=[('', 'Select Year'), ('firstyear', 'First Year'), ('secondyear', 'Second Year'), ('thirdyear', 'Third Year'), ('fourthyear', 'Fourth Year')], default='', max_length=50, null=True)),
                ('branch', models.CharField(blank=True, choices=[('', 'Select Branch'), ('cse', 'Computer Engg.'), ('ee', 'Electrical Engg.'), ('ece', 'Electronics and Comm. Engg.'), ('me', 'Mechanical Engg.'), ('pie', 'Production and Industial Engg.'), ('ce', 'Civil Engg.')], default='', max_length=50, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('rollno', models.CharField(max_length=10, null=True, unique=True)),
                ('myassignments', models.ManyToManyField(to='assignment.Assignment')),
                ('student_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]