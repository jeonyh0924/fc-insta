# Generated by Django 3.0.7 on 2020-07-13 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentlike',
            name='like_count',
        ),
        migrations.AddField(
            model_name='comment',
            name='like_count',
            field=models.IntegerField(default=0),
        ),
    ]