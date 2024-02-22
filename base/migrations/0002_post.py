# Generated by Django 4.1.7 on 2023-05-30 19:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('postimage', models.ImageField(upload_to='postimage')),
                ('caption', models.CharField(max_length=500)),
                ('no_of_likes', models.IntegerField(default=0)),
            ],
        ),
    ]
