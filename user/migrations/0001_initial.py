<<<<<<< HEAD
# Generated by Django 2.2.4 on 2019-08-04 02:01
=======
# Generated by Django 2.2.3 on 2019-08-02 07:40
>>>>>>> dc84e8139e636d82e443dd9023a52cbf1e311c7d

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD
        ('assignment', '0001_initial'),
        ('auth', '0011_update_proxy_permissions'),
=======
>>>>>>> dc84e8139e636d82e443dd9023a52cbf1e311c7d
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
<<<<<<< HEAD
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
=======
>>>>>>> dc84e8139e636d82e443dd9023a52cbf1e311c7d
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('year', models.CharField(blank=True, choices=[('', 'Select Year'), ('firstyear', 'First Year'), ('secondyear', 'Second Year'), ('thirdyear', 'Third Year'), ('fourthyear', 'Fourth Year')], default='', max_length=50, null=True)),
                ('branch', models.CharField(blank=True, choices=[('', 'Select Branch'), ('cse', 'Computer Engg.'), ('ee', 'Electrical Engg.'), ('ece', 'Electronics and Comm. Engg.'), ('me', 'Mechanical Engg.'), ('pie', 'Production and Industial Engg.'), ('ce', 'Civil Engg.')], default='', max_length=50, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('rollno', models.CharField(max_length=10, null=True, unique=True)),
<<<<<<< HEAD
                ('is_teacher', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('myassignments', models.ManyToManyField(to='assignment.Assignment')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
=======
                ('admin', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
>>>>>>> dc84e8139e636d82e443dd9023a52cbf1e311c7d
            ],
            options={
                'abstract': False,
            },
        ),
    ]
