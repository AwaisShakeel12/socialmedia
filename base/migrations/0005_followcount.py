# Generated by Django 4.1.7 on 2023-06-02 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_likepost'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('follower', models.CharField(max_length=100)),
            ],
        ),
    ]
