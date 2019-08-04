# Generated by Django 2.2.4 on 2019-08-04 02:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phonenumber', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('user.user',),
        ),
    ]