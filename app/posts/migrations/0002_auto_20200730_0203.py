# Generated by Django 3.0.7 on 2020-07-30 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_query_name='posts', to='posts.Tag'),
        ),
    ]