# Generated by Django 4.2.1 on 2023-05-12 00:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_followings'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmarked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarked', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
